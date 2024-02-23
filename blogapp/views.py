from django.shortcuts import render ,redirect , get_object_or_404
from .forms import CustomUserForm , LoginForm , PostForm , CommentForm , CustomUpdateUserForm ,ResetForm , CustomResetUpdateUserForm , ContactForm
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


#email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from .models import CustomUser ,Post , Comment , Categories



def newpassword(request):
    if request.method == 'POST':
        form = CustomResetUpdateUserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']

            if password == password1:
                uid = request.session.get('uid')
                user = CustomUser.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request,'Password reset successfully,please login.Thank you.')
                return redirect('Signin')

            else:
                messages.error(request,'Passwords do not match')
                return redirect('NewPassword')

    else:
        form = CustomResetUpdateUserForm()
    context = {'form':form}
    return render(request,'blogapp/resetpasswordform.html',context)



def resetpasswordtoken(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('NewPassword')
    else:
        messages.error(request,'This link has been expired!')
        return redirect('Resetpassword')



def resetpassword(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email__exact=email)

                #User Forgot Activation
                current_site = get_current_site(request)
                mail_subject = 'Reset your password'
                message = render_to_string('blogapp/resetver.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMultiAlternatives(mail_subject,message,to=[to_email])
                send_email.attach_alternative(message, "text/html")
                send_email.send()

                messages.success(request,'Password reset email has been sent to your email address')
                return redirect('Signin')
            else:
                messages.error(request,'Account does not exist!')
                return redirect('Resetpassword')
    else:
        form = ResetForm()
    context = {'form':form}            
    return render(request,'blogapp/forgotpassword.html',context)


@login_required
def deletecom(request,id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('Home')


def category(request, strr):
    category_obj = get_object_or_404(Categories, name=strr)
    posts = Post.objects.filter(categories=category_obj)
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    context = {'strr': strr, 'posts': paginated_posts,'data':posts}
    return render(request, 'blogapp/category.html', context)



def search(request):
    if request.method == 'GET':
        search_text = request.GET.get('searchtext')
        # Perform case-insensitive search across title, content, and categories
        search_result = Post.objects.filter(
            Q(title__icontains=search_text) | 
            Q(content__icontains=search_text) |
            Q(categories__name__icontains=search_text)
        ).distinct()  # Remove duplicate results
        
    context = {'search_result': search_result, 'search_text': search_text}
    return render(request, 'blogapp/search-result.html', context)


def accmanagement(request):
    user = request.user
    post = Post.objects.all().filter(author=user)
    count = post.count()
    if request.method == 'POST':
        form = CustomUpdateUserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
    else:
        form = CustomUpdateUserForm(instance=user)
    context = {'count':count,'form':form}
    return render(request,'blogapp/accmanagement.html',context)



@login_required
def updateblog(request, id=None):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST': 
        fm = PostForm(request.POST,request.FILES,instance=post)
        if fm.is_valid():
            fm.save()
            return redirect('Managebogs')
    else:
        fm = PostForm(instance=post)
    context = {'form': fm,'post':post}
    return render(request, 'blogapp/updateblog.html', context)

@login_required
def managebogs(request):
    user = request.user
    post = Post.objects.all().filter(author=user)
    context = {'data':post}
    return render(request,'blogapp/managebogs.html',context)


@login_required
def addblog(request):
    if request.method == 'POST':
        fm = PostForm(request.POST, request.FILES)
        if fm.is_valid():
            post = fm.save(commit=False)
            post.author = request.user
            post.save()
         
            messages.info(request, 'Your blog has been added. Thank you!')
            return redirect('Addblog')
    else:
        fm = PostForm()
    context = {'form': fm}
    return render(request, 'blogapp/addblog.html', context)



def logoutuser(request):
    logout(request)
    return redirect('Home')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:  # Ensure user is not already active
            user.is_active = True
            user.save()
            # Mark the token as used here
            # You might want to have a field in your CustomUser model to store the token status
            messages.success(request, 'Congratulations! Your account is activated.')
        else:
            messages.error(request, 'Your account is already activated.')
    else:
        messages.error(request, 'Invalid activation link')
    return redirect('Signin')





def home(request):
    two_days_ago = timezone.now() - timedelta(days=2)
    posts_list = Post.objects.annotate(num_comments=models.Count('comments')).order_by('-created_at')
    paginator = Paginator(posts_list, 10)  
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'two_days_ago': two_days_ago}
    return render(request, 'blogapp/home.html', context)



def about(request):
    return render(request,'blogapp/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Contact') 
    else:
        form = ContactForm()
    context = {'form': form}    
    return render(request, 'blogapp/contact.html',context)



def singlepost(request, title):
    # Get the current post
    data = get_object_or_404(Post, title=title)

    # Retrieve comments related to the current post
    cdata = Comment.objects.filter(post=data)

    # Retrieve related posts excluding the current post
    rpost = Post.objects.exclude(id=data.id).filter(categories=data.categories)

    if request.method == 'POST':
        fm = CommentForm(request.POST)
        if fm.is_valid():
            post = fm.save(commit=False)
            post.author = request.user
            post.post = data  # Assign the Post instance directly
            post.save()
            return redirect('Singlepost', title=title)
    else:
        fm = CommentForm()
        
    context = {'data': data, 'cdata': cdata, 'form': fm, 'rpost': rpost}
    return render(request, 'blogapp/singlepost.html', context)



def register(request):
    if request.method == 'POST':
        fm = CustomUserForm(request.POST,request.FILES)
        if fm.is_valid():
            user = fm.save()
            password = fm.cleaned_data.get('password')
            user.set_password(password)  # Set the password
            user.save()  

            #User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('blogapp/accountverification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = user.email
            send_email = EmailMultiAlternatives(mail_subject,message,to=[to_email])
            send_email.attach_alternative(message, "text/html")
            send_email.send()
            return redirect('/register/?command=verification&email='+to_email)  
    else:
        fm = CustomUserForm()        
    context = {'form':fm}
    return render(request,'blogapp/register.html',context)



def signin(request):
    if request.method == 'POST':
        fm = LoginForm(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('Home')
            else:
                messages.error(request,'Invalid credentials. Please check your email and password!')
    else:
        fm = LoginForm()    
    context = {'form':fm}
    return render(request,'blogapp/signin.html',context)

