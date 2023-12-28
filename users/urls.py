from django.urls import path, include
from users import views

urlpatterns = [

    path('accounts/', include('allauth.urls'), name='login'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('discovery/', views.DiscoveryView.as_view(), name="discovery"),
    path('create_tours/', views.create_tours, name="create_tours"),
    path('delete_tour/<int:tour_id>/', views.delete_tour, name='delete_tour'),
    path('save_tour/', views.save_tour, name='save_tour'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('search_locations/', views.search_locations, name='search_locations'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('start_tour/<int:tour_id>/', views.start_tour, name='start_tour'),
    path('rate_location/<int:pk>/', views.rate_location, name='rate_location'),
]