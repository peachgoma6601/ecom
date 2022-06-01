from django.urls import path
from . import views
# from rest_framework.authtoken.views import obtain_auth_token 

# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register, name='register'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('forgotpassword/',views.forgotpassword,name='forgot_password'),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),

    # path('auth-token/',obtain_auth_token),
    # path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    # path('api/token/refresh',TokenRefreshView.as_view(),name='token_refresh')

    ]