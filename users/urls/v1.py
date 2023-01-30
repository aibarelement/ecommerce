from django.urls import path
from users import views


urlpatterns = [
    path('users/create/', views.UserViewSet.as_view({'post': 'create_user'})),
    path('users/create-token/', views.UserViewSet.as_view({'post': 'create_token'})),
    path('users/', views.UserViewSet.as_view({'get': 'get_user'}))
]
