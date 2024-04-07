from django.urls import path
from .views import *

urlpatterns = [
    path('mainmodels/', MainModelListView.as_view(), name='mainmodel-list'),
    path('mainmodels/<str:pk>', MainModelListViewDetail.as_view(), name='mainmodel-detail'),
    path('mainmodels_delete/<str:pk>', MainModelDeleteView.as_view(), name='mainmodel-delete'),
    
]
