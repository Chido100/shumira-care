from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('item_details/<int:pk>/', views.item_details, name='item-details'),
    path('new_item/', views.new_item, name='new-item'),
    path('edit_item/<int:pk>/', views.edit_item, name='edit-item'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete-item'),

    path('about_us/', views.about_us, name='about-us'),
]