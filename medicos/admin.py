from django.contrib import admin
from medicos.models import Especialidad, Medico, Agenda

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre']  # Cambiado 'nome' a 'nombre' para consistencia en español.

class MedicoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'crm', 'telefono',  # Cambiado a español.
    ]
    search_fields = ['nombre', 'crm']  # Permitir búsqueda por nombre y CRM.

class AgendaAdmin(admin.ModelAdmin):
    list_display = [
        'dia', 'medico', 'horario'  # Campos en español.
    ]
    list_filter = ['dia', 'medico']  # Filtrar por día y médico.
    ordering = ['dia']  # Ordenar las agendas por fecha.

admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Agenda, AgendaAdmin)
