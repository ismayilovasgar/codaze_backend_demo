from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class CustomUser(AbstractUser):
    # Yeni eklenen özel  validator-lar
    phone_regex = RegexValidator(
        # regex=r"^\+?1?\d{9,15}$",
        regex=r"^\+?[0-9]{9,20}$",
        message="Telefon numarası '+999999999' formatında olmalıdır. En fazla 20 basamak olabilir.",
    )

    def strong_password_validator(password):
        if len(password) < 8:
            raise ValidationError(_("Şifre en az 8 karakter uzunluğunda olmalıdır."))
        if not re.search(r"[A-Z]", password):
            raise ValidationError(_("Şifre en az bir büyük harf içermelidir."))
        if not re.search(r"[a-z]", password):
            raise ValidationError(_("Şifre en az bir küçük harf içermelidir."))
        if not re.search(r"[0-9]", password):
            raise ValidationError(_("Şifre en az bir rakam içermelidir."))
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_("Şifre en az bir özel karakter içermelidir."))

    # def user_attribute_similarity_validator(password, user):
    #     if user.username.lower() in password.lower() or user.email.split('@')[0].lower() in password.lower():
    #         raise ValidationError(_('Şifre, kullanıcı adı veya e-posta ile çok benzer olmamalıdır.'))

    # Varsayılan User alanları
    id = models.BigAutoField(primary_key=True)  # Otomatik birincil anahtar.
    username = models.CharField(max_length=150, unique=True)  # Kullanıcı adı.
    first_name = models.CharField(max_length=150, blank=True)  # İsim.
    last_name = models.CharField(max_length=150, blank=True)  # Soyisim.
    email = models.EmailField(blank=True, unique=True)  # E-posta adresi.
    password = models.CharField(
        max_length=128, validators=[strong_password_validator]
    )  # Şifre (hash'lenmiş).
    is_staff = models.BooleanField(default=False)  # Admin erişimi.
    is_active = models.BooleanField(default=True)  # Hesap aktif mi?
    is_superuser = models.BooleanField(default=False)  # Süper kullanıcı mı?
    last_login = models.DateTimeField(null=True, blank=True)  # Son giriş zamanı.
    date_joined = models.DateTimeField(auto_now_add=True)  # Katılma tarihi.
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

    # def set_password(self, raw_password):
    #     user_attribute_similarity_validator(raw_password, self)
    #     super().set_password(raw_password)

    # todo: -------------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return self.username

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
