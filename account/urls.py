from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name="account"),
    path('products/', views.products, name='products'),
    path('customers/<str:id>', views.customers, name='customers'),
    path('create_order/<str:id>', views.createOrder, name='create_order'),
    path('update_order/<str:id>', views.updateOrder, name='update_order'),
    path('delete_order/<str:id>', views.deleteOrder, name='delete_order'),
    
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', 
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'), name='password_reset_complete'),
]