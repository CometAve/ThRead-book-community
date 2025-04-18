from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('<int:user_pk>/change_password/', views.change_password, name='change_password'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
