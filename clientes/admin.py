from django.contrib import admin
from .models import Cliente, Consulta

class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nif', 'telefono', 'sexo'  # Campos adaptados al español
    ]
    search_fields = ['nif', 'usuario__username']  # Permitir búsquedas por NIF o nombre de usuario

class ConsultaAdmin(admin.ModelAdmin):
    list_display = [
        'agenda', 'cliente'  # Campos adaptados al español
    ]
    list_filter = ['agenda', 'cliente']  # Agregar filtros por agenda y cliente

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Consulta, ConsultaAdmin)
