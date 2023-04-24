from .views import *
from django.urls import path

app_name = "daftar"
urlpatterns = [
    path('kunjungan/', daftarKunjungan, name='daftarKunjungan'),
    path('terapis/', daftarTerapis, name='daftarTerapis'),
]