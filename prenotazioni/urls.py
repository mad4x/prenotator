from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addBooking, name='add'),
    path('list/', views.listBookings, name='list'),
    path('list-active/', views.listActiveBookings, name='list-active'),
    path('list-archived/', views.listArchivedBookings, name='list-archived'),
    path('list-by-name/<str:name>', views.listBookingsByName, name='list-by-name'),
    path('list-by-date/<str:date>', views.listBookingsByDate, name='list-by-date'),
    path('delete/<int:id>/', views.deleteBooking, name='delete'),
    path('update/<int:id>/', views.updateBooking, name='update')
]
