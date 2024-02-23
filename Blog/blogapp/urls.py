from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blogapp import views


urlpatterns = [

    path('',views.home,name='Home'),
    path('about/',views.about,name='About'),
    path('blog/<str:title>/', views.singlepost, name='Singlepost'),
    path('blog/<str:title>/<int:id>/', views.singlepost, name='Singlepost'),
    path('contact/',views.contact,name='Contact'),
    path('signin/',views.signin,name='Signin'),
    path('register/',views.register,name='Register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logoutuser/',views.logoutuser,name='Logout'),
    path('addblog/',views.addblog,name='Addblog'),
    path('managebogs/',views.managebogs,name='Managebogs'),
    path('updateblog/<int:id>/',views.updateblog,name='Updateblog'),
    path('accmanagement/',views.accmanagement,name='Accmanagement'),
    path('search/',views.search,name='Search'),
    path('category/<str:strr>/',views.category,name='Category'),
    path('remvingcomment/<int:id>/',views.deletecom,name='Delete'),

    path('resetpassword/',views.resetpassword,name='Resetpassword'),
    path('resetpasswordtoken/<uidb64>/<token>/', views.resetpasswordtoken, name='ResetPasswordtoken'),

    path('newpassword/',views.newpassword,name='NewPassword'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



