from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from daftar_terapi.models import *
from account.models import *
from rekam_medis.models import *
from django.db.models import Q
from django.utils.timezone import localtime, now
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from django.core.files.storage import FileSystemStorage


def editDataDiri(request):
    pass

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
    list_asesmen = []
    pasien = Pasien.objects.get(id=idPasien)
    rekamMedis = RekamMedis.objects.get(pasien=pasien)
    
    if Asesmen.objects.filter(pasien=pasien).first() != None:
            for asesmen in Asesmen.objects.filter(pasien=pasien):
                list_asesmen.append(asesmen)
                
    if request.user.role == 'Terapis':
        terapis = Terapis.objects.get(user=request.user)
        if terapis in rekamMedis.terapis.all():
            if request.method == 'POST':
                
                
                fs = FileSystemStorage()
                file_Asesmen = request.FILES.get('lampiran')
                filename = fs.save(file_Asesmen.name, file_Asesmen)
                existing_file = Asesmen.objects.filter(pasien=pasien, tipe=request.POST.get('tipe'))
                if existing_file:     
                    existing_file.update(lampiran=file_Asesmen, tanggal_dibuat=datetime.now())
                else:
                    list_asesmen.append(
                        Asesmen.objects.create(
                            pasien=pasien,
                            terapis=terapis,
                            tipe=request.POST.get('tipe'),
                            lampiran=file_Asesmen, 
                            tanggal_dibuat=datetime.now(),
                        )
                    )
                
                return redirect('dasbor:rekamMedisView', idPasien=idPasien)
            else:
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
        'list_asesmen' : list_asesmen,
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
        list_asesmen = []
        pasien = Pasien.objects.get(user=request.user)
        rekamMedis = RekamMedis.objects.get(pasien=pasien)
        kunjunganAll = Appointment.objects.filter(
                Q(status=1) | Q(status=0),
                pasien=pasien,
        )
        if Asesmen.objects.filter(pasien=pasien).first() != None:
            for asesmen in Asesmen.objects.filter(pasien=pasien):
                list_asesmen.append(asesmen)
                
        context = {
            'pasien' : pasien,
            'kunjunganAll' : kunjunganAll,
            'message' : message,
            'rekamMedis' : rekamMedis,
            'list_asesmen' : list_asesmen,
        }
        return render(request, "dasbor-pasien.html", context)
    
    else:
        message = "Kamu tidak memiliki akses ke halaman ini."
        context = {
            'message' : message,
        }
        return render(request, "dasbor-admin.html", context)
    