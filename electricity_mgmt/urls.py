from django.urls import path
from . import views
 


urlpatterns = [
      path('login', views.view_login, name='login'),
      path('logout', views.user_logout, name='logout'),
      path('register', views.register, name='register'),

      path('createApplication', views.createApplication, name="createApplication"),
      path('ApplicationListview', views.ApplicationListview, name="ApplicationListview"),
      path('updateApplication/<id>', views.updateApplication, name="updateApplication/<id>"),
]