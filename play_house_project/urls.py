from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from play_house_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('halls/', views.hall_list, name='hall_list'),
    path('booking/', views.create_booking, name='create_booking'),
    path('', views.inf, name='inf'),
    path("halls/<int:pk>/", views.hall_detail, name="hall_detail"), 
    path("booking/<int:place_id>/", views.create_bookingg, name="create_booking_with_place"),
    path("place/<int:place_id>/", views.place_detail, name="place_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)