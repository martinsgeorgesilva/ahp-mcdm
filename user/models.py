from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
import datetime
import uuid



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('encarregado', 'Encarregado'),
        ('operario', 'Operário'),
        ('gerente', 'Gerente'),
    )
    occupation = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES, 
        default=TYPE_CHOICES[0][0], 
        verbose_name='Qual o seu perfil?'
    )
    company = models.CharField(
        max_length=20, 
        verbose_name='Empresa', 
        null=True, 
        blank=True
    )
    email = models.EmailField(unique=True)
    joined = models.DateField(default=datetime.date.today)
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})