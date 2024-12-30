from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addBooking, name='add'),
    path('list/', views.listBookings, name='list'),
    path('delete/<int:id>/', views.deleteBooking, name='delete')
]