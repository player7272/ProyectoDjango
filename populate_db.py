"""
Script para poblar la base de datos de BMS con datos de prueba realistas
Ejecutar con: python manage.py shell < populate_db.py
"""

from django.contrib.auth.models import User
from core1.models import Estado, Persona, Categoria, Solicitud
from core2.models import Empleado, TipoPermiso, Permiso, PeriodoNomina, Nomina
from core3.models import ConfiguracionNomina
from decimal import Decimal
from datetime import date, timedelta
import random

print("🚀 Iniciando población de base de datos...")

# ============================================
# 1. CREAR ESTADOS
# ============================================
print("\n📋 Creando estados del sistema...")
estados_nombres = ['Pendiente', 'Aprobado', 'Rechazado', 'En Proceso']
estados = {}
for nombre in estados_nombres:
    estado, created = Estado.objects.get_or_create(nombre=nombre)
    estados[nombre] = estado
    if created:
        print(f"   ✓ Estado creado: {nombre}")

# ============================================
# 2. CREAR CATEGORÍAS
# ============================================
print("\n💼 Creando categorías de empleados...")
categorias_data = [
    {
        'nombre': 'Desarrollador Junior',
        'descripcion': 'Desarrollador con 0-2 años de experiencia en tecnologías web y móviles.',
        'salario_base': Decimal('2000000.00')
    },
    {
        'nombre': 'Desarrollador Senior',
        'descripcion': 'Desarrollador con más de 5 años de experiencia liderando proyectos técnicos.',
        'salario_base': Decimal('4000000.00')
    },
    {
        'nombre': 'Analista de Datos',
        'descripcion': 'Especialista en análisis de datos, estadística y machine learning.',
        'salario_base': Decimal('3500000.00')
    },
    {
        'nombre': 'Gerente de Proyectos',
        'descripcion': 'Responsable de la planificación y ejecución de proyectos tecnológicos.',
        'salario_base': Decimal('5000000.00')
    },
    {
        'nombre': 'DevOps Engineer',
        'descripcion': 'Especialista en automatización, CI/CD y gestión de infraestructura cloud.',
        'salario_base': Decimal('3800000.00')
    },
    {
        'nombre': 'Diseñador UX/UI',
        'descripcion': 'Diseñador especializado en experiencia de usuario e interfaces.',
        'salario_base': Decimal('3000000.00')
    }
]

categorias = {}
for cat_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults={
            'descripcion': cat_data['descripcion'],
            'salario_base': cat_data['salario_base']
        }
    )
    categorias[cat_data['nombre']] = categoria
    if created:
        print(f"   ✓ Categoría creada: {cat_data['nombre']} (${cat_data['salario_base']})")

# ============================================
# 3. CREAR TIPOS DE PERMISOS
# ============================================
print("\n⏰ Creando tipos de permisos...")
tipos_permisos_data = [
    {
        'nombre': 'Vacaciones',
        'descripcion': 'Días de vacaciones acumulados por el empleado.',
        'dias_maximos': 15,
        'requiere_aprobacion': True
    },
    {
        'nombre': 'Permiso Médico',
        'descripcion': 'Permiso por razones médicas o citas de salud.',
        'dias_maximos': 10,
        'requiere_aprobacion': True
    },
    {
        'nombre': 'Permiso Personal',
        'descripcion': 'Permiso para atender asuntos personales o familiares.',
        'dias_maximos': 5,
        'requiere_aprobacion': True
    },
    {
        'nombre': 'Permiso de Estudio',
        'descripcion': 'Permiso para asistir a capacitaciones o estudios formales.',
        'dias_maximos': 0,  # Sin límite
        'requiere_aprobacion': True
    }
]

tipos_permisos = {}
for tipo_data in tipos_permisos_data:
    tipo, created = TipoPermiso.objects.get_or_create(
        nombre=tipo_data['nombre'],
        defaults={
            'descripcion': tipo_data['descripcion'],
            'dias_maximos': tipo_data['dias_maximos'],
            'requiere_aprobacion': tipo_data['requiere_aprobacion']
        }
    )
    tipos_permisos[tipo_data['nombre']] = tipo
    if created:
        print(f"   ✓ Tipo de permiso creado: {tipo_data['nombre']}")

# ============================================
# 4. CREAR EMPLEADOS
# ============================================
print("\n👥 Creando empleados...")

empleados_data = [
    ('María', 'García', '1234567890', 'maria.garcia@bms.com', 'Desarrollador Senior'),
    ('Carlos', 'López', '0987654321', 'carlos.lopez@bms.com', 'Gerente de Proyectos'),
    ('Ana', 'Martínez', '1122334455', 'ana.martinez@bms.com', 'Analista de Datos'),
    ('Luis', 'Rodríguez', '5544332211', 'luis.rodriguez@bms.com', 'DevOps Engineer'),
    ('Laura', 'Hernández', '9988776655', 'laura.hernandez@bms.com', 'Diseñador UX/UI'),
    ('Jorge', 'González', '1357924680', 'jorge.gonzalez@bms.com', 'Desarrollador Senior'),
    ('Patricia', 'Ramírez', '2468013579', 'patricia.ramirez@bms.com', 'Desarrollador Junior'),
    ('Roberto', 'Torres', '3692581470', 'roberto.torres@bms.com', 'DevOps Engineer'),
    ('Carmen', 'Flores', '7412589630', 'carmen.flores@bms.com', 'Analista de Datos'),
    ('Diego', 'Vargas', '8523697410', 'diego.vargas@bms.com', 'Desarrollador Senior'),
    ('Sofía', 'Castro', '9517538520', 'sofia.castro@bms.com', 'Diseñador UX/UI'),
    ('Miguel', 'Morales', '1593574560', 'miguel.morales@bms.com', 'Gerente de Proyectos'),
    ('Valentina', 'Jiménez', '7536951480', 'valentina.jimenez@bms.com', 'Desarrollador Junior'),
    ('Andrés', 'Ruiz', '3571594560', 'andres.ruiz@bms.com', 'DevOps Engineer'),
    ('Isabella', 'Mendoza', '9513574680', 'isabella.mendoza@bms.com', 'Analista de Datos'),
    ('Fernando', 'Ortiz', '7539514680', 'fernando.ortiz@bms.com', 'Desarrollador Senior'),
    ('Camila', 'Silva', '1597538460', 'camila.silva@bms.com', 'Diseñador UX/UI'),
    ('Javier', 'Rojas', '3579512460', 'javier.rojas@bms.com', 'Desarrollador Junior'),
    ('Natalia', 'Gutiérrez', '7531598460', 'natalia.gutierrez@bms.com', 'DevOps Engineer'),
    ('Gabriel', 'Medina', '9517532680', 'gabriel.medina@bms.com', 'Analista de Datos'),
    ('Daniela', 'Reyes', '1234509876', 'daniela.reyes@bms.com', 'Desarrollador Senior'),
    ('Sebastián', 'Cruz', '9876543210', 'sebastian.cruz@bms.com', 'Gerente de Proyectos'),
    ('Valeria', 'Díaz', '1472583690', 'valeria.diaz@bms.com', 'Desarrollador Junior'),
    ('Mateo', 'Pérez', '7418529630', 'mateo.perez@bms.com', 'DevOps Engineer'),
    ('Lucía', 'Sánchez', '3698521470', 'lucia.sanchez@bms.com', 'Analista de Datos'),
    ('Santiago', 'Ramírez', '8529637410', 'santiago.ramirez@bms.com', 'Desarrollador Senior'),
    ('Martina', 'Herrera', '7539518460', 'martina.herrera@bms.com', 'Diseñador UX/UI'),
    ('Nicolás', 'Acosta', '1593578460', 'nicolas.acosta@bms.com', 'Desarrollador Junior'),
    ('Emma', 'Campos', '3571598460', 'emma.campos@bms.com', 'DevOps Engineer'),
    ('Matías', 'Vega', '9513578460', 'matias.vega@bms.com', 'Analista de Datos'),
]

empleados = []
fecha_base = date(2023, 1, 1)

for i, (nombre, apellido, cedula, correo, categoria_nombre) in enumerate(empleados_data):
    # Crear usuario
    username = correo
    password = cedula
    
    try:
        user = User.objects.create_user(
            username=username,
            email=correo,
            password=password,
            first_name=nombre,
            last_name=apellido
        )
        
        # Crear empleado
        fecha_ingreso = fecha_base + timedelta(days=random.randint(0, 730))  # Hasta 2 años atrás
        fecha_nacimiento = date(random.randint(1985, 2000), random.randint(1, 12), random.randint(1, 28))
        
        empleado = Empleado.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            correo=correo,
            telefono=f"300{random.randint(1000000, 9999999)}",
            direccion=f"Calle {random.randint(1, 200)} #{random.randint(1, 100)}-{random.randint(1, 99)}",
            fecha_nacimiento=fecha_nacimiento,
            fecha_ingreso=fecha_ingreso,
            categoria=categorias[categoria_nombre],
            activo=True,
            datos_completados=True
        )
        
        empleados.append(empleado)
        print(f"   ✓ Empleado creado: {nombre} {apellido} ({categoria_nombre})")
        
    except Exception as e:
        print(f"   ✗ Error al crear empleado {nombre} {apellido}: {e}")

print(f"\n✅ Total de empleados creados: {len(empleados)}")

# ============================================
# 5. CREAR CONFIGURACIÓN DE NÓMINA
# ============================================
print("\n⚙️ Creando configuración de nómina...")
config, created = ConfiguracionNomina.objects.get_or_create(
    activo=True,
    defaults={
        'porcentaje_seguridad_social': Decimal('4.0'),
        'porcentaje_salud': Decimal('4.0'),
        'porcentaje_pension': Decimal('4.0'),
        'valor_auxilio_transporte': Decimal('140606.00'),
        'salario_minimo_legal': Decimal('1300000.00')
    }
)
if created:
    print("   ✓ Configuración de nómina creada")

# ============================================
# 6. CREAR PERIODOS DE NÓMINA Y NÓMINAS
# ============================================
print("\n💰 Creando periodos de nómina y nóminas...")

# Crear 4 periodos mensuales (últimos 4 meses)
periodos = []
fecha_actual = date.today()

for i in range(4, 0, -1):
    # Calcular fechas del periodo
    mes = fecha_actual.month - i
    ano = fecha_actual.year
    
    if mes <= 0:
        mes += 12
        ano -= 1
    
    # Primer y último día del mes
    fecha_inicio = date(ano, mes, 1)
    
    if mes == 12:
        fecha_fin = date(ano, 12, 31)
    else:
        fecha_fin = date(ano, mes + 1, 1) - timedelta(days=1)
    
    # Fecha de pago: 5 días después del fin del mes
    fecha_pago = fecha_fin + timedelta(days=5)
    
    periodo, created = PeriodoNomina.objects.get_or_create(
        tipo='MENSUAL',
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        defaults={
            'fecha_pago': fecha_pago,
            'cerrado': i > 2  # Los dos últimos están abiertos
        }
    )
    
    periodos.append(periodo)
    if created:
        print(f"   ✓ Periodo creado: {periodo}")

# Crear nóminas para cada empleado en cada periodo
nominas_creadas = 0
for periodo in periodos:
    for empleado in empleados:
        salario_base = empleado.categoria.salario_base
        
        # Calcular deducciones según configuración
        deducciones = (
            salario_base * (config.porcentaje_seguridad_social / 100) +
            salario_base * (config.porcentaje_salud / 100) +
            salario_base * (config.porcentaje_pension / 100)
        )
        
        # Bonificaciones aleatorias (20% de empleados)
        bonificaciones = Decimal(random.choice([0, 0, 0, 0, random.randint(100000, 500000)]))
        
        # Horas extra aleatorias (30% de empleados)
        if random.random() < 0.3:
            horas_extra = Decimal(random.randint(5, 20))
            valor_hora_extra = salario_base / Decimal('240')  # Asumiendo 240 horas mensuales
        else:
            horas_extra = Decimal('0')
            valor_hora_extra = Decimal('0')
        
        total_devengado = salario_base + bonificaciones + (horas_extra * valor_hora_extra)
        neto_pagar = total_devengado - deducciones
        
        # Determinar si está pagado (periodos cerrados están pagados)
        pagado = periodo.cerrado
        
        nomina, created = Nomina.objects.get_or_create(
            empleado=empleado,
            periodo=periodo,
            defaults={
                'salario_base': salario_base,
                'bonificaciones': bonificaciones,
                'deducciones': deducciones,
                'horas_extra': horas_extra,
                'valor_hora_extra': valor_hora_extra,
                'total_devengado': total_devengado,
                'total_deducciones': deducciones,
                'neto_pagar': neto_pagar,
                'pagado': pagado
            }
        )
        
        if created:
            nominas_creadas += 1

print(f"   ✓ {nominas_creadas} nóminas creadas")

# ============================================
# 7. CREAR PERMISOS
# ============================================
print("\n⏰ Creando permisos...")

estados_permiso = ['PENDIENTE', 'APROBADO', 'RECHAZADO']
motivos = [
    "Necesito atender asuntos médicos personales",
    "Tengo una emergencia familiar que requiere mi atención",
    "Deseo tomar días de descanso acumulados",
    "Debo asistir a capacitación profesional",
    "Tengo cita médica programada",
    "Necesito resolver asuntos personales urgentes",
    "Viaje familiar programado con anticipación",
    "Asistir a conferencia tecnológica",
    "Cita médica especializada",
    "Trámites personales importantes"
]

permisos_creados = 0
fecha_base_permiso = date.today() - timedelta(days=90)

# Crear entre 1 y 3 permisos por empleado
for empleado in random.sample(empleados, min(25, len(empleados))):  # 25 empleados con permisos
    num_permisos = random.randint(1, 3)
    
    for _ in range(num_permisos):
        tipo_permiso = random.choice(list(tipos_permisos.values()))
        
        # Fecha de inicio aleatoria en los últimos 3 meses
        dias_desde_base = random.randint(0, 90)
        fecha_inicio = fecha_base_permiso + timedelta(days=dias_desde_base)
        
        # Duración del permiso
        if tipo_permiso.dias_maximos > 0:
            duracion = random.randint(1, tipo_permiso.dias_maximos)
        else:
            duracion = random.randint(1, 5)
        
        fecha_fin = fecha_inicio + timedelta(days=duracion - 1)
        
        # Estado del permiso (más aprobados que rechazados)
        estado = random.choices(
            estados_permiso,
            weights=[0.2, 0.6, 0.2],  # 20% pendiente, 60% aprobado, 20% rechazado
            k=1
        )[0]
        
        observaciones_map = {
            'APROBADO': [
                "Permiso aprobado. Disfruta tu tiempo libre.",
                "Aprobado. Recuerda gestionar tus pendientes antes de salir.",
                "Permiso concedido sin inconvenientes.",
            ],
            'RECHAZADO': [
                "Lo sentimos, en estas fechas hay mucha carga laboral.",
                "No es posible aprobar el permiso en este momento. Por favor reprograma.",
                "Rechazado por conflicto con entregas importantes del proyecto.",
            ],
            'PENDIENTE': ["", "", ""]
        }
        
        permiso = Permiso.objects.create(
            empleado=empleado,
            tipo_permiso=tipo_permiso,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            motivo=random.choice(motivos),
            estado=estado,
            observaciones=random.choice(observaciones_map[estado]),
            fecha_respuesta=fecha_inicio - timedelta(days=1) if estado != 'PENDIENTE' else None
        )
        
        permisos_creados += 1

print(f"   ✓ {permisos_creados} permisos creados")

# ============================================
# 8. CREAR SOLICITUDES DE EMPLEO
# ============================================
print("\n📋 Creando solicitudes de empleo...")

nombres_candidatos = [
    ('Pedro', 'Sánchez'), ('Lucía', 'Fernández'), ('Manuel', 'Gómez'),
    ('Rosa', 'Martín'), ('Antonio', 'López'), ('Teresa', 'García'),
    ('Francisco', 'Rodríguez'), ('María José', 'Pérez'), ('José Luis', 'Hernández'),
    ('Pilar', 'González'), ('Juan Carlos', 'Díaz'), ('Isabel', 'Ruiz'),
    ('Rafael', 'Jiménez'), ('Dolores', 'Moreno'), ('Ángel', 'Muñoz'),
    ('Mercedes', 'Álvarez'), ('Enrique', 'Romero'), ('Cristina', 'Navarro'),
    ('Alberto', 'Torres'), ('Beatriz', 'Domínguez'), ('Ricardo', 'Vázquez'),
    ('Silvia', 'Ramos'), ('Raúl', 'Gil'), ('Gloria', 'Serrano'),
    ('Ignacio', 'Blanco'), ('Mónica', 'Castro'), ('Héctor', 'Ortega')
]

mensajes_solicitud = [
    """Soy desarrollador full-stack con 3 años de experiencia en React, Node.js y PostgreSQL. 
    He trabajado en proyectos de e-commerce y aplicaciones móviles. Tengo certificaciones en AWS.""",
    
    """Graduado en Ingeniería de Sistemas con especialización en ciencia de datos. 
    Experiencia en Python, machine learning y visualización de datos con Power BI.""",
    
    """Diseñador UX/UI con portfolio en Behance. Experiencia en Figma, Adobe XD y 
    metodologías de design thinking. He trabajado para startups y empresas establecidas.""",
    
    """Desarrollador junior entusiasta con conocimientos en Java, Spring Boot y Angular. 
    Recién graduado buscando oportunidad para crecer profesionalmente.""",
    
    """DevOps engineer con experiencia en Docker, Kubernetes, Jenkins y terraform. 
    He implementado pipelines CI/CD para proyectos de gran escala.""",
    
    """Gerente de proyectos certificado PMP con 5 años liderando equipos ágiles. 
    Experiencia en metodologías Scrum y Kanban.""",
    
    """Analista de datos con experiencia en SQL, Python y R. He trabajado en proyectos 
    de business intelligence y predicción de demanda."""
]

solicitudes_creadas = 0
cedulas_usadas = set(emp.cedula for emp in empleados)

for i, (nombre, apellido) in enumerate(nombres_candidatos[:25]):  # Crear 25 solicitudes
    # Generar cédula única
    cedula = str(random.randint(1000000000, 9999999999))
    while cedula in cedulas_usadas:
        cedula = str(random.randint(1000000000, 9999999999))
    cedulas_usadas.add(cedula)
    
    correo = f"{nombre.lower().replace(' ', '.')}.{apellido.lower()}@email.com"
    
    # Crear persona
    persona, created = Persona.objects.get_or_create(
        cedula=cedula,
        defaults={
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo
        }
    )
    
    # Crear solicitud
    categoria = random.choice(list(categorias.values()))
    estado = random.choices(
        ['Pendiente', 'Aprobado', 'Rechazado'],
        weights=[0.4, 0.4, 0.2],  # 40% pendiente, 40% aprobado, 20% rechazado
        k=1
    )[0]
    
    fecha_creacion = date.today() - timedelta(days=random.randint(1, 60))
    
    solicitud = Solicitud.objects.create(
        persona=persona,
        mensaje=random.choice(mensajes_solicitud),
        estado=estados[estado],
        categoria=categoria,
        fecha_creacion=fecha_creacion
    )
    
    solicitudes_creadas += 1

print(f"   ✓ {solicitudes_creadas} solicitudes creadas")

# ============================================
# RESUMEN FINAL
# ============================================
print("\n" + "="*50)
print("✅ POBLACIÓN DE BASE DE DATOS COMPLETADA")
print("="*50)
print(f"\n📊 Resumen:")
print(f"   • Estados del sistema: {Estado.objects.count()}")
print(f"   • Categorías de empleados: {Categoria.objects.count()}")
print(f"   • Tipos de permisos: {TipoPermiso.objects.count()}")
print(f"   • Empleados creados: {Empleado.objects.count()}")
print(f"   • Periodos de nómina: {PeriodoNomina.objects.count()}")
print(f"   • Nóminas generadas: {Nomina.objects.count()}")
print(f"   • Permisos creados: {Permiso.objects.count()}")
print(f"   • Solicitudes de empleo: {Solicitud.objects.count()}")
print(f"\n💡 Credenciales de acceso:")
print(f"   Empleados: {empleados[0].correo} / {empleados[0].cedula}")
print(f"   (Todos los empleados usan su cédula como contraseña)")
print("\n🎉 ¡Base de datos lista para usar!")
print("="*50)