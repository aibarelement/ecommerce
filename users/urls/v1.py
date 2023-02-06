from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users import views


urlpatterns = [
    path('users/create/', views.UserViewSet.as_view({'post': 'create_user'})),
    # path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/', views.UserViewSet.as_view({'post': 'create_token'})),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
