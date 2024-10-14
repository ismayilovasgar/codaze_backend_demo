from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    # Varsayılan User alanları
    id = models.BigAutoField(primary_key=True)  # Otomatik birincil anahtar.
    username = models.CharField(max_length=150, unique=True)  # Kullanıcı adı.
    first_name = models.CharField(max_length=150, blank=True)  # İsim.
    last_name = models.CharField(max_length=150, blank=True)  # Soyisim.
    email = models.EmailField(blank=True, unique=True)  # E-posta adresi.
    password = models.CharField(max_length=128)  # Şifre (hash'lenmiş).
    is_staff = models.BooleanField(default=False)  # Admin erişimi.
    is_active = models.BooleanField(default=True)  # Hesap aktif mi?
    is_superuser = models.BooleanField(default=False)  # Süper kullanıcı mı?
    last_login = models.DateTimeField(null=True, blank=True)  # Son giriş zamanı.
    date_joined = models.DateTimeField(auto_now_add=True)  # Katılma tarihi.

    # Yeni eklenen özel alan
    phone_regex = RegexValidator(
        # regex=r"^\+?1?\d{9,15}$",
        regex=r"^\+?[0-9]{9,20}$",
        message="Telefon numarası '+999999999' formatında olmalıdır. En fazla 20 basamak olabilir.",
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )

    # Şifreyi set ederken hash'lemek için
    def set_password(self, raw_password):
        super().set_password(raw_password)

    # -------------------------------------------------------------------
    def __str__(self):
        return self.username

    def __str__(self):
        return f"{self.first_name}"

    # groups = models.ManyToManyField(
    #     "auth.Group",
    #     related_name="customuser_set",  # Değiştirin
    #     blank=True,
    #     help_text="The groups this user belongs to.",
    #     verbose_name="groups",
    # )

    # user_permissions = models.ManyToManyField(
    #     "auth.Permission",
    #     related_name="customuser_set",  # Değiştirin
    #     blank=True,
    #     help_text="Specific permissions for this user.",
    #     verbose_name="user permissions",
    # )


class Note(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notes",
    )
    title = models.CharField(max_length=100, null=True, blank=True)
    cover_image = models.ImageField(upload_to="images/", null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False, null=True, blank=True)

    # This is the string representation of the object
    def __str__(self):
        return self.title
