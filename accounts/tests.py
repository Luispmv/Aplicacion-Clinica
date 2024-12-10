from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import date, timedelta
from clientes.models import Cliente, Consulta  # Importación de los modelos Cliente y Consulta
from medicos.models import Agenda, Especialidad, Medico  # Importación de los modelos relacionados con médicos
from .models import User  # Importación del modelo de usuario personalizado


# Pruebas para el modelo de usuario
class UserModelTest(TestCase):
    def setUp(self):
        # Configuración inicial: Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            name='Test User'
        )
    
    def test_user_creation(self):
        # Verifica que los campos del usuario se hayan configurado correctamente
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_user_str(self):
        # Verifica que el método _str_ devuelva el nombre correctamente
        self.assertEqual(str(self.user), 'Test User')


# Pruebas para el modelo Cliente
class ClienteModelTest(TestCase):
    def setUp(self):
        # Configuración inicial: Crear un usuario y un cliente
        self.user = User.objects.create_user(
            username='clientuser',
            password='password123',
            email='clientuser@example.com',
            name='Client User'
        )
        self.cliente = Cliente.objects.create(
            sexo='MAS',
            telefono='+12345678901',
            nif='12345678909',
            usuario=self.user
        )
    
    def test_cliente_creation(self):
        # Verifica que los campos del cliente se hayan configurado correctamente
        self.assertEqual(self.cliente.usuario.username, 'clientuser')
        self.assertEqual(self.cliente.sexo, 'MAS')
        self.assertEqual(self.cliente.telefono, '+12345678901')

    def test_cliente_str(self):
        # Verifica que el método _str_ devuelva el nombre de usuario correctamente
        self.assertEqual(str(self.cliente), 'clientuser')


# Pruebas para el modelo Especialidad
class EspecialidadModelTest(TestCase):
    def setUp(self):
        # Configuración inicial: Crear una especialidad
        self.especialidad = Especialidad.objects.create(nombre='Cardiología')
    
    def test_especialidad_creation(self):
        # Verifica que el campo nombre de la especialidad sea correcto
        self.assertEqual(self.especialidad.nombre, 'Cardiología')

    def test_especialidad_str(self):
        # Verifica que el método _str_ devuelva el nombre correctamente
        self.assertEqual(str(self.especialidad), 'Cardiología')


# Pruebas para el modelo Medico
class MedicoModelTest(TestCase):
    def setUp(self):
        # Configuración inicial: Crear una especialidad y un médico
        self.especialidad = Especialidad.objects.create(nombre='Neurología')
        self.medico = Medico.objects.create(
            nombre='Dr. Juan Pérez',
            correo_electronico='drjuan@example.com',
            crm='12345',
            telefono='+12345678901',
            especialidad=self.especialidad
        )
    
    def test_medico_creation(self):
        # Verifica que los campos del médico sean correctos
        self.assertEqual(self.medico.nombre, 'Dr. Juan Pérez')
        self.assertEqual(self.medico.especialidad.nombre, 'Neurología')

    def test_medico_str(self):
        # Verifica que el método _str_ devuelva el nombre correctamente
        self.assertEqual(str(self.medico), 'Dr. Juan Pérez')


# Pruebas para el modelo Agenda
class AgendaModelTest(TestCase):
    def setUp(self):
        # Configuración inicial: Crear un usuario, una especialidad, un médico y una agenda
        self.user = User.objects.create_user(
            username='doctoruser',
            password='password123',
            email='doctoruser@example.com',
            name='Doctor User'
        )
        self.especialidad = Especialidad.objects.create(nombre='Pediatría')
        self.medico = Medico.objects.create(
            nombre='Dra. Ana López',
            correo_electronico='dralopez@example.com',
            crm='54321',
            telefono='+12345678901',
            especialidad=self.especialidad
        )
        self.agenda = Agenda.objects.create(
            medico=self.medico,
            dia=date.today() + timedelta(days=1),  # Día futuro
            horario='1',
            usuario=self.user
        )
    
    def test_agenda_creation(self):
        # Verifica que los campos de la agenda sean correctos
        self.assertEqual(self.agenda.medico.nombre, 'Dra. Ana López')
        self.assertEqual(self.agenda.horario, '1')

    def test_agenda_unique_together(self):
        # Verifica que no se puedan crear entradas duplicadas para el mismo horario y día
        with self.assertRaises(ValidationError):
            duplicate_agenda = Agenda(
                medico=self.medico,
                dia=self.agenda.dia,
                horario=self.agenda.horario,
                usuario=self.user
            )
            duplicate_agenda.full_clean()  # Lanza un error de validación


# Pruebas para el modelo Consulta
class ConsultaModelTest(TestCase):
    def setUp(self):
        # Configuración inicial: Crear un usuario, un cliente, un médico, una agenda y una consulta
        self.user = User.objects.create_user(
            username='clientuser',
            password='password123',
            email='clientuser@example.com',
            name='Client User'
        )
        self.cliente = Cliente.objects.create(
            sexo='FEM',
            telefono='+9876543210',
            nif='98765432109',
            usuario=self.user
        )
        self.especialidad = Especialidad.objects.create(nombre='Dermatología')
        self.medico = Medico.objects.create(
            nombre='Dr. Roberto García',
            correo_electronico='drroberto@example.com',
            crm='67890',
            telefono='+12345678901',
            especialidad=self.especialidad
        )
        self.agenda = Agenda.objects.create(
            medico=self.medico,
            dia=date.today() + timedelta(days=2),  # Día futuro
            horario='2',
            usuario=self.user
        )
        self.consulta = Consulta.objects.create(
            agenda=self.agenda,
            cliente=self.cliente
        )
    
    def test_consulta_creation(self):
        # Verifica que los campos de la consulta sean correctos
        self.assertEqual(self.consulta.cliente.usuario.username, 'clientuser')
        self.assertEqual(self.consulta.agenda.medico.nombre, 'Dr. Roberto García')

    def test_consulta_unique_together(self):
        # Verifica que no se puedan crear consultas duplicadas para la misma agenda y cliente
        with self.assertRaises(ValidationError):
            duplicate_consulta = Consulta(
                agenda=self.agenda,
                cliente=self.cliente
            )
            duplicate_consulta.full_clean()  # Lanza un error de validación