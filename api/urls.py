from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from api import views

urlpatterns = [
    path('', views.HelloView.as_view(), name='hello'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
