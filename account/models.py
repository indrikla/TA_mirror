from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

ROLE_CHOICES = (
    ("Admin", "Admin"),
    ("Pasien", "Pasien"),
    ("Terapis", "Terapis"),
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a `User` with an email, username and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')


        user = self.create_user(
            email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model, overrided from django.contrib.auth.models.User."""

    email = models.EmailField(
        'email address',
        unique=True,
        blank=False,
        error_messages={
            'unique': "A user with that email already exists.",
    })
    full_name = models.CharField(
        'full name',
        max_length=150,
        blank=False
    )
    role = models.CharField(
        'role',
        max_length=50,
        blank=False,
        choices=ROLE_CHOICES
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)


    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name for the user."""
        return self.full_name

    def get_role(self):
        """Return the role of the user."""
        return self.role


SPESIALISASI_CHOICES = (
    ("Fisioterapi", "Fisioterapi"),
    ("Terapi Okupasi", "Terapi Okupasi"),
    ("Terapi Wicara", "Terapi Wicara"),
)
GENDER_CHOICES = (
    ("Laki-Laki", "Laki-Laki"),
    ("Perempuan", "Perempuan"),
)

TIPE_CHOICES = (
    ("Anak", "Anak"),
    ("Dewasa", "Dewasa"),
)

STATUS_CHOICES = (
    ("Umum", "Umum"),
    ("Mahasiswa", "Mahasiswa"),
    ("Pekerja di Vokasi UI", "Pekerja di Vokasi UI"),
    ("Pekerja di UI non Vokasi", "Pekerja di UI non Vokasi"),
)


def jsonfield_default_value(): 
    return {0: 'Hari'}

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = "", null=True, blank=True)
    name = models.CharField('Nama', max_length=50, null=True, blank=False)
    
    class Meta:
        db_table = 'Admin'
        
    def __str__(self):
        return self.name


class Terapis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = "", null=True, blank=True)
    name = models.CharField('Nama', max_length=50, null=True, blank=False)
    spesialisasi = models.CharField('Spesialisasi', null=True, blank=False, max_length=50, choices=SPESIALISASI_CHOICES)
    jadwal_hari = models.JSONField("Jadwal Hari", default=jsonfield_default_value)

    class Meta:
        db_table = 'Terapis'
        
    def __str__(self):
        return self.name


class Wali_Pasien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = "", null=True, blank=True)
    name = models.CharField('Nama', max_length=50, null=True, blank=False)
    jenis_kelamin = models.CharField('Jenis Kelamin', null=True, blank=False, max_length=20, choices=GENDER_CHOICES)
    hubungan = models.CharField('Hubungan', null=True, blank=False, max_length=50)
    nomor_whatsapp = models.CharField('Nomor WhatsApp', null=True, blank=False, max_length=25)
    alamat = models.CharField('Alamat', null=True, blank=False, max_length=250)
    email_wali = models.EmailField()
    pekerjaan = models.CharField('Pekerjaan', null=True, blank=False, max_length=50)
    
    class Meta:
        db_table = 'Wali_Pasien'
    
    def __str__(self):
        return self.name


class Pasien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = "", null=True, blank=True)
    name = models.CharField('Nama', max_length=50, null=True, blank=False)
    tipe = models.CharField('Tipe', null=True, blank=False, max_length=50, choices=TIPE_CHOICES)
    tanggal_lahir = models.DateField(validators=[
        MaxValueValidator(date.today),
        MinValueValidator(date.today().replace(year=date.today().year - 100))
    ])
    tempat_lahir = models.CharField('Tempat Lahir', null=True, blank=False, max_length=50)
    jenis_kelamin = models.CharField('Jenis Kelamin', null=True, blank=False, max_length=20, choices=GENDER_CHOICES)
    nomor_whatsapp = models.CharField('Nomor WhatsApp', null=True, blank=False, max_length=25)
    alamat = models.CharField('Alamat', null=True, blank=False, max_length=250)
    pekerjaan = models.CharField('Pekerjaan', null=True, blank=False, max_length=50)
    status = models.CharField('Status', null=True, blank=False, max_length=50, choices=STATUS_CHOICES)
    wali = models.ForeignKey(
        Wali_Pasien, on_delete=models.SET_NULL, null=True, blank=True, related_name="wali")
    
    class Meta:
        db_table = 'Pasien'
        
    def __str__(self):
        return self.name