from django.contrib import admin
from django.urls import path
from .views import DoctorView, PatientView, VisitView
from rest_framework.authtoken import views
# from .views import ItemListCreateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    # path('item/', ItemListCreateView.as_view()),
    path('doctor/', DoctorView.as_view(
                                    {'get':'list',
                                     'post':'create'})),
    path('doctor/<int:id>/', DoctorView.as_view(
                            {'get': 'retrieve',
                            'post': 'update',
                            'delete':'destroy'})),
    path('doctor/<int:id>/patient', DoctorView.as_view(
                            {'get': 'list_patient'}) ),


    path('patient/', PatientView.as_view(
        {'get': 'list',
         'post': 'create'})),
    path('patient/<int:id>/', PatientView.as_view(
        {'get': 'retrieve',
         'post': 'update',
         'delete': 'destroy'})),

    path('visit/', VisitView.as_view(
        {'get': 'create'})),

    # path('token/', views.obtain_auth_token)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
