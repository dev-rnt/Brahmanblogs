from django import forms
from blogapp.models import CustomUser , Post , Categories , Comment , Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class ResetForm(forms.Form):
    email = forms.EmailField(label=' ',label_suffix=' ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email'}))


class CustomResetUpdateUserForm(forms.ModelForm):
    password1 = forms.CharField(label=' ',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm new password'}))
    password = forms.CharField(label=' ',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your new password'}))
    class Meta:
        model = CustomUser
        fields = ['password']


class CustomUpdateUserForm(forms.ModelForm):
    img = forms.ImageField(label=' ',error_messages={'required': 'Profile pic required'},label_suffix=' ',widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','phone','img']
        widgets = {

        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),               
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content':forms.Textarea(attrs={'class': 'form-control','placeholder':'share your review','rows':3,'cols':3})
        }



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'video', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }



class LoginForm(forms.Form):
    email = forms.EmailField(label='',label_suffix='',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    password = forms.CharField(label='',label_suffix='',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    img = forms.ImageField(label=' ',error_messages={'required': 'Profile pic required'},label_suffix=' ',widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','phone','img','password']
        widgets = {

        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),                  
                  }

           
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password!= password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
