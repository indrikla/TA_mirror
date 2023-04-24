from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from daftar_terapi.models import *
from account.models import *
from rekam_medis.models import RekamMedis
from django.db.models import Q
from django.utils.timezone import localtime, now
from django.views.decorators.csrf import csrf_exempt


def editDataDiri(request):
    pasien = Pasien.objects.filter(user=request.user)
    
    if request.method == 'POST':
        pass
    else:
        pass
    context = {
        'pasien' : pasien[0]
    }
    return render(request, "edit-data-diri.html", context)

def updateStatusKunjungan(request, idKunjungan, toBeStatus):
    '''
    Updating status sequentially
    (0 Menunggu Konfirmasi -> 1 Dikonfirmasi -> 2 Sedang Berlangsung -> 3 Menunggu Pembayaran -> 4 Selesai)
    (5 Menunggu Pembatalan -> 6 Dibatalkan)
    (1 Dikonfirmasi -> 7 Tidak Hadir)
    '''    
    updatedKunjungan = Appointment.objects.get(id=idKunjungan)
    if (toBeStatus <= 4):
        updatedKunjungan.status = updatedKunjungan.status + 1
    else:
        updatedKunjungan.status = toBeStatus
        
    updatedKunjungan.save()
    return redirect('dasbor:dasbor')


def rekamMedisView(request, idPasien):
    message = ""
    kunjunganAll = []
    pasien = Pasien.objects.get(id=idPasien)
    rekamMedis = RekamMedis.objects.get(pasien=pasien)
    
    if request.user.role == 'Terapis':
        terapis = Terapis.objects.get(user=request.user)
        if terapis in rekamMedis.terapis.all():
            pass
        else:
            message = "Kamu tidak memiliki akses ke halaman ini."
            
    elif request.user.role == 'Pasien':
        if (idPasien == request.user.pasien.id):
            pasien = Pasien.objects.get(user=request.user)
            kunjunganAll = Appointment.objects.filter(
                Q(status=1) | Q(status=0),
                pasien=pasien,
            )
        else:
            message = "Kamu tidak memiliki akses ke halaman ini."
        
    context = {
        'pasien' : pasien,
        'kunjunganAll' : kunjunganAll,
        'message' : message,
        'rekamMedis' : rekamMedis,
    }
    return render(request, "list-rekam-medis.html", context)

def detailRekamMedis(request, idPasien, idKunjungan):
    message = ""
    pasien = Pasien.objects.get(id=idPasien)
    kunjunganDetail = Appointment.objects.filter(
        id=idKunjungan,
        pasien=pasien,
    )
    context = {
        'pasien' : pasien,
        'message' : message,
        'kunjunganDetail' : kunjunganDetail[0],
    }
    if request.method == 'POST':
        # Terapi yang Sedang Berlangsung akan otomatis Selesai bila Terapis telah memverifikasi pengisian Rekam Medis pasien
        if request.POST.get('verifikasi') and kunjunganDetail[0].status == 2:
            k = kunjunganDetail[0]
            k.status = 3
            k.save()
            
        kunjunganDetail.update(
            pemeriksaan = request.POST.get('pemeriksaan'),
            tindakan = request.POST.get('tindakan'),
            evaluasi_terapi = request.POST.get('evaluasi_terapi'),
            catatan_terapi = request.POST.get('catatan_terapi'),
            verifikasi = request.POST.get('verifikasi'),
        )
        return render(request, "detail-rekam-medis-edit.html", context)
    else:
        if request.user.role == 'Pasien':
            return render(request, "detail-rekam-medis-view.html", context)
        else:
            return render(request, "detail-rekam-medis-edit.html", context)
    
    
    
def dasbor(request):
    message = ""
    if request.user.role == 'Terapis':
        terapis = Terapis.objects.get(user=request.user)
        kunjunganToday = Appointment.objects.filter(
            status=1, 
            tanggal_terapi=str(localtime(now()).date()), 
            terapis=terapis
        ).order_by('slot_waktu')
        
        kunjunganSelesai = Appointment.objects.filter(
            Q(status=2) | Q(status=3),
            verifikasi=False,
            tanggal_terapi=str(localtime(now()).date()), 
            terapis=terapis
        ).order_by('slot_waktu')
        context = {
            'terapis' : terapis,
            'kunjunganToday' : kunjunganToday,
            'waktu' : str(localtime(now()).strftime("%X")),
            'today' : str(localtime(now()).strftime("%A, %d %B %Y %T")),
            'kunjunganSelesai' : kunjunganSelesai,
        }
        return render(request, "dasbor-terapis.html", context)
    
    elif request.user.role == 'Admin':
        admin = Admin.objects.get(user=request.user)
        kunjungan_mp = Appointment.objects.filter(
            status=3,
        ).order_by('tanggal_terapi')
        
        kunjungan_mk = Appointment.objects.filter(
            status=0,
        ).order_by('tanggal_terapi')
        context = {
            'waktu' : str(localtime(now()).strftime("%X")),
            'today' : str(localtime(now()).strftime("%A, %d %B %Y %T")),
            'kunjungan_mk' : kunjungan_mk,
            'kunjungan_mp' : kunjungan_mp,
        }
        return render(request, "dasbor-admin.html", context)
    
    elif request.user.role == 'Pasien':
        pasien = Pasien.objects.get(user=request.user)
        rekamMedis = RekamMedis.objects.get(pasien=pasien)
        kunjunganAll = Appointment.objects.filter(
                Q(status=1) | Q(status=0),
                pasien=pasien,
        )
        context = {
            'pasien' : pasien,
            'kunjunganAll' : kunjunganAll,
            'message' : message,
            'rekamMedis' : rekamMedis,
        }
        return render(request, "dasbor-pasien.html", context)
    
    else:
        message = "Kamu tidak memiliki akses ke halaman ini."
        context = {
            'message' : message,
        }
        return render(request, "dasbor-admin.html", context)
    