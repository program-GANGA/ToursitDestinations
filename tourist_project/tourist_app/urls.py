from django.urls import path
from . views import *
from . import views


urlpatterns=[
    path('create/', TouristCreateView.as_view(), name="create_tourist"),
    path('detail/<int:pk>/', TouristDetailsView.as_view(), name="detail_view"),
    path('update/<int:pk>/', TouristUpdateView.as_view(), name="update_tourist"),
    path('delete/<int:pk>/', TouristDeleteView.as_view(), name="delete_tourist"),
    path('search/<str:placename>/',TouristSearch.as_view(),name="search_tourist"),


path('',views.index,name='base'),
path('createtour/', views.create_tour, name='create_tour'),
path('details/<int:id>/',tourist_detail, name='detail'), 
path('deleted/<int:id>/',tourist_delete, name='delete'),
path('updatetour/<int:id>/',tourist_update,name='update'),

]
