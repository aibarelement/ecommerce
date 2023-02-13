from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from users import views


urlpatterns = [
    path('users/create/', views.UserViewSet.as_view({'post': 'create_user'})),
    path('users/verify/', views.UserViewSet.as_view({'post': 'verify_user'})),
    path('users/token/', views.UserViewSet.as_view({'post': 'create_token'})),
    path('users/token/verify/', views.UserViewSet.as_view({'post': 'verify_token'})),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
]
