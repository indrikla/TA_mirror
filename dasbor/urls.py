from .views import *
from django.urls import path

app_name = "dasbor"
urlpatterns = [
    path('', dasbor, name='dasbor'),
    path('update/<int:idKunjungan>/<int:toBeStatus>', updateStatusKunjungan, name='updateStatusKunjungan'),
    path('rme/<int:idPasien>', rekamMedisView, name='rekamMedisView'),
    path('rme/<int:idPasien>/detail-<int:idKunjungan>', detailRekamMedis, name='detailRekamMedis'),
    path('data-diri/edit', editDataDiri, name='editDataDiri'),
]