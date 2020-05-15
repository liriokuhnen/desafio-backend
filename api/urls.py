from api import views

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('travel/', views.TravelView.as_view(), name='get_travel'),
    path('travel/<int:travel_id>/', views.TravelView.as_view(), name='update_travel'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
