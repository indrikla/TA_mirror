from django.shortcuts import render
from daftar_terapi.models import *
from account.models import *
from rekam_medis.models import RekamMedis
from django.db.models import Q
from django.utils.timezone import localtime, now
from django.core.paginator import Paginator, EmptyPage

# Create your views here.

def daftarKunjungan(request):
    kunjunganAll = []
    
    if request.user.role == 'Terapis':
        terapis = Terapis.objects.get(user=request.user)
        kunjunganAll = Appointment.objects.filter(
            terapis=terapis
        )
        
    elif request.user.role == 'Pasien':
        pasien = Pasien.objects.get(user=request.user)
        kunjunganAll = Appointment.objects.filter(
            pasien=pasien
        )
    else:
        kunjunganAll = Appointment.objects.all()
    
    menungguKonfirmasi = kunjunganAll.filter(
        status=0
    )
    dikonfirmasi = kunjunganAll.filter(
        status=1
    )
    menungguPembatalan = kunjunganAll.filter(
        status=5
    )
    menungguPembayaran = kunjunganAll.filter(
        status=3
    )    
    
    p = Paginator(kunjunganAll, 20)
    page_num = request.GET.get('page', 1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
    context = {
        'kunjungan' : page,
        'kunjunganAll' : kunjunganAll,
        'menungguKonfirmasi' : menungguKonfirmasi,
        'dikonfirmasi' : dikonfirmasi,
        'menungguPembatalan' : menungguPembatalan,
        'menungguPembayaran' : menungguPembayaran,
    }
    
    return render(request, "daftar-kunjungan.html", context)

def daftarTerapis(request):
    terapisAll = Terapis.objects.all()
    
    ft = terapisAll.filter(
        spesialisasi="Fisioterapi"
    )
    ot = terapisAll.filter(
        spesialisasi="Terapi Okupasi"
    )
    tw = terapisAll.filter(
        spesialisasi="Terapi Wicara"
    )
    p = Paginator(terapisAll, 20)
    page_num = request.GET.get('page', 1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
    context = {
        'terapis' : page,
        'terapisAll' : terapisAll,
        'ot' : ot,
        'ft' : ft,
        'tw' : tw,
    }
    return render(request, "daftar-terapis.html", context)