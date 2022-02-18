from django.urls import path
from .views import city_delete, index
urlpatterns = [
    path('',index,name='indexpage'),
    path('delete/<int:id>',city_delete,name='delete')
]