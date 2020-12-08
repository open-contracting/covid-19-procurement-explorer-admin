from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('total_contracts/', views.TotalContractsView.as_view()),
    path('total_spending/', views.TotalSpendingsView.as_view()),
]