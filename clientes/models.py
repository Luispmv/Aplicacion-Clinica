from django.conf import settings
from django.db.models.fields.related import ForeignKey, OneToOneField
from django_cpf_cnpj.fields import CPFField
from django.core.validators import RegexValidator
from django.db import models
from medicos.models import Agenda

class Cliente(models.Model):
    SEXO = (
        ("MAS", "Masculino"),
        ("FEM", "Femenino")
    )
    
    sexo = models.CharField(max_length=9, choices=SEXO, verbose_name="Sexo")
    
    validador_telefono = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número debe estar en este formato: '+99 99 9999-0000'."
    )
    telefono = models.CharField(
        verbose_name="Teléfono",
        validators=[validador_telefono],
        max_length=17,
        null=True,
        blank=True
    )
    
    nif = CPFField(
        verbose_name="NIF",
        max_length=50,
        unique=True
    )
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name='Usuario', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.usuario.username}'  # Asume que el modelo de usuario tiene un campo "username"

class Consulta(models.Model):
    agenda = OneToOneField(
        Agenda,
        on_delete=models.CASCADE,
        related_name='consulta',
        verbose_name="Agenda"
    )
    cliente = ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='consulta',
        verbose_name="Cliente"
    )
    
    class Meta:
        unique_together = ('agenda', 'cliente')
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        
    def __str__(self):
        return f'{self.agenda} - {self.cliente}'
