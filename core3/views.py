from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Sum, Count
from decimal import Decimal

from core1.models import Solicitud, Persona, Estado
from core2.models import Empleado, Permiso, Nomina, PeriodoNomina, ConceptoNomina
from .models import ProcesoContratacion, ConfiguracionNomina
from .forms import (
    RevisionSolicitudForm, ContratacionForm, RevisionPermisoForm,
    PeriodoNominaForm, NominaManualForm, ConceptoNominaForm,
    ConfiguracionNominaForm
)

# Decorador para verificar si el usuario es staff (RRHH)
def es_rrhh(user):
    return user.is_staff or user.is_superuser

# ========== DASHBOARD ==========
@login_required
@user_passes_test(es_rrhh)
def dashboard_rrhh(request):
    """Dashboard principal de Recursos Humanos"""
    # Estadísticas generales
    solicitudes_pendientes = Solicitud.objects.filter(
        estado__nombre='Pendiente'
    ).count()
    
    permisos_pendientes = Permiso.objects.filter(
        estado='PENDIENTE'
    ).count()
    
    empleados_activos = Empleado.objects.filter(activo=True).count()
    empleados_totales = Empleado.objects.count()
    
    # Últimas actividades
    ultimas_solicitudes = Solicitud.objects.all().order_by('-fecha_creacion')[:5]
    ultimos_permisos = Permiso.objects.all().order_by('-fecha_solicitud')[:5]
    
    # Nóminas pendientes de pago
    nominas_pendientes = Nomina.objects.filter(pagado=False).count()
    
    context = {
        'solicitudes_pendientes': solicitudes_pendientes,
        'permisos_pendientes': permisos_pendientes,
        'empleados_activos': empleados_activos,
        'empleados_totales': empleados_totales,
        'ultimas_solicitudes': ultimas_solicitudes,
        'ultimos_permisos': ultimos_permisos,
        'nominas_pendientes': nominas_pendientes,
    }
    
    return render(request, 'core3/dashboard.html', context)


# ========== GESTIÓN DE SOLICITUDES ==========
@login_required
@user_passes_test(es_rrhh)
def lista_solicitudes(request):
    """Lista todas las solicitudes de empleo"""
    filtro = request.GET.get('estado', 'todas')
    
    solicitudes = Solicitud.objects.all().select_related('persona', 'estado', 'categoria')
    
    if filtro == 'pendientes':
        solicitudes = solicitudes.filter(estado__nombre='Pendiente')
    elif filtro == 'aprobadas':
        solicitudes = solicitudes.filter(estado__nombre='Aprobado')
    elif filtro == 'rechazadas':
        solicitudes = solicitudes.filter(estado__nombre='Rechazado')
    
    solicitudes = solicitudes.order_by('-fecha_creacion')
    
    context = {
        'solicitudes': solicitudes,
        'filtro_actual': filtro,
    }
    
    return render(request, 'core3/solicitudes/lista.html', context)


@login_required
@user_passes_test(es_rrhh)
def revisar_solicitud(request, solicitud_id):
    """Revisar y aprobar/rechazar una solicitud"""
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    
    # Crear o obtener proceso de contratación
    proceso, created = ProcesoContratacion.objects.get_or_create(
        solicitud=solicitud,
        defaults={'revisado_por': request.user}
    )
    
    if request.method == 'POST':
        form = RevisionSolicitudForm(request.POST, instance=proceso)
        if form.is_valid():
            decision = request.POST.get('decision')
            proceso = form.save(commit=False)
            proceso.fecha_decision = timezone.now()
            proceso.revisado_por = request.user
            
            if decision == 'APROBAR':
                proceso.estado_proceso = 'APROBADO'
                # Cambiar estado de la solicitud
                estado_aprobado, _ = Estado.objects.get_or_create(nombre='Aprobado')
                solicitud.estado = estado_aprobado
                solicitud.save()
                messages.success(request, f'Solicitud de {solicitud.persona.nombre} APROBADA para contratación.')
                proceso.save()
                return redirect('contratar_empleado', solicitud_id=solicitud.id)
            
            elif decision == 'RECHAZAR':
                proceso.estado_proceso = 'RECHAZADO'
                estado_rechazado, _ = Estado.objects.get_or_create(nombre='Rechazado')
                solicitud.estado = estado_rechazado
                solicitud.save()
                messages.warning(request, f'Solicitud de {solicitud.persona.nombre} RECHAZADA.')
            
            proceso.save()
            return redirect('lista_solicitudes_rrhh')
    else:
        form = RevisionSolicitudForm(instance=proceso)
    
    context = {
        'solicitud': solicitud,
        'proceso': proceso,
        'form': form,
    }
    
    return render(request, 'core3/solicitudes/revisar.html', context)


@login_required
@user_passes_test(es_rrhh)
def contratar_empleado(request, solicitud_id):
    """Crear empleado y usuario desde una solicitud aprobada"""
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    proceso = get_object_or_404(ProcesoContratacion, solicitud=solicitud)
    
    if proceso.estado_proceso != 'APROBADO':
        messages.error(request, 'Esta solicitud no ha sido aprobada.')
        return redirect('lista_solicitudes_rrhh')
    
    if proceso.empleado_creado:
        messages.info(request, 'Este empleado ya fue contratado previamente.')
        return redirect('detalle_empleado_rrhh', empleado_id=proceso.empleado_creado.id)
    
    if request.method == 'POST':
        # Pre-cargar datos de la solicitud
        datos_iniciales = {
            'nombre': solicitud.persona.nombre,
            'apellido': solicitud.persona.apellido,
            'cedula': solicitud.persona.cedula,
            'correo': solicitud.persona.correo,
            'categoria': solicitud.categoria,
        }
        
        form = ContratacionForm(request.POST, initial=datos_iniciales)
        
        if form.is_valid():
            # Crear usuario (correo como username, cédula como contraseña)
            username = form.cleaned_data['correo']
            password = form.cleaned_data['cedula']
            
            try:
                # Verificar si ya existe un usuario con ese correo
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Ya existe un usuario con ese correo.')
                    return render(request, 'core3/solicitudes/contratar.html', {'form': form, 'solicitud': solicitud})
                
                # Crear usuario
                user = User.objects.create_user(
                    username=username,
                    email=username,
                    password=password,
                    first_name=form.cleaned_data['nombre'],
                    last_name=form.cleaned_data['apellido']
                )
                
                # Crear empleado
                empleado = form.save(commit=False)
                empleado.user = user
                empleado.activo = True
                empleado.datos_completados = True
                empleado.save()
                
                # Actualizar proceso de contratación
                proceso.estado_proceso = 'CONTRATADO'
                proceso.empleado_creado = empleado
                proceso.save()
                
                messages.success(
                    request,
                    f'¡Empleado {empleado.nombre} {empleado.apellido} contratado exitosamente! '
                    f'Usuario: {username} | Contraseña: {password}'
                )
                
                return redirect('detalle_empleado_rrhh', empleado_id=empleado.id)
            
            except Exception as e:
                messages.error(request, f'Error al crear el empleado: {str(e)}')
    
    else:
        # Pre-cargar el formulario con datos de la solicitud
        form = ContratacionForm(initial={
            'nombre': solicitud.persona.nombre,
            'apellido': solicitud.persona.apellido,
            'cedula': solicitud.persona.cedula,
            'correo': solicitud.persona.correo,
            'categoria': solicitud.categoria,
        })
    
    context = {
        'form': form,
        'solicitud': solicitud,
        'proceso': proceso,
    }
    
    return render(request, 'core3/solicitudes/contratar.html', context)


# ========== GESTIÓN DE PERMISOS ==========
@login_required
@user_passes_test(es_rrhh)
def lista_permisos(request):
    """Lista todos los permisos solicitados por empleados"""
    filtro = request.GET.get('estado', 'todos')
    
    permisos = Permiso.objects.all().select_related('empleado', 'tipo_permiso')
    
    if filtro == 'pendientes':
        permisos = permisos.filter(estado='PENDIENTE')
    elif filtro == 'aprobados':
        permisos = permisos.filter(estado='APROBADO')
    elif filtro == 'rechazados':
        permisos = permisos.filter(estado='RECHAZADO')
    
    permisos = permisos.order_by('-fecha_solicitud')

    # 🔹 Cálculos de estadísticas para la tabla
    total_permisos = Permiso.objects.count()
    permisos_pendientes = Permiso.objects.filter(estado='PENDIENTE').count()
    permisos_aprobados = Permiso.objects.filter(estado='APROBADO').count()
    permisos_rechazados = Permiso.objects.filter(estado='RECHAZADO').count()

    # 🔹 Evitar división por cero
    if total_permisos > 0:
        porcentaje_permisos_pendientes = round((permisos_pendientes / total_permisos) * 100, 2)
        porcentaje_permisos_aprobados = round((permisos_aprobados / total_permisos) * 100, 2)
        porcentaje_permisos_rechazados = round((permisos_rechazados / total_permisos) * 100, 2)
    else:
        porcentaje_permisos_pendientes = porcentaje_permisos_aprobados = porcentaje_permisos_rechazados = 0

    context = {
        'permisos': permisos,
        'filtro_actual': filtro,
        'total_permisos': total_permisos,
        'permisos_pendientes': permisos_pendientes,
        'permisos_aprobados': permisos_aprobados,
        'permisos_rechazados': permisos_rechazados,
        'porcentaje_permisos_pendientes': porcentaje_permisos_pendientes,
        'porcentaje_permisos_aprobados': porcentaje_permisos_aprobados,
        'porcentaje_permisos_rechazados': porcentaje_permisos_rechazados,
    }
    
    return render(request, 'core3/permisos/lista.html', context)


@login_required
@user_passes_test(es_rrhh)
def revisar_permiso(request, permiso_id):
    """Revisar y aprobar/rechazar un permiso de empleado"""
    permiso = get_object_or_404(Permiso, id=permiso_id)
    
    if request.method == 'POST':
        form = RevisionPermisoForm(request.POST, instance=permiso)
        if form.is_valid():
            decision = request.POST.get('decision')
            permiso = form.save(commit=False)
            permiso.fecha_respuesta = timezone.now()
            
            if decision == 'APROBADO':
                permiso.estado = 'APROBADO'
                messages.success(request, f'Permiso de {permiso.empleado.nombre} APROBADO.')
            elif decision == 'RECHAZADO':
                permiso.estado = 'RECHAZADO'
                messages.warning(request, f'Permiso de {permiso.empleado.nombre} RECHAZADO.')
            
            permiso.save()
            return redirect('lista_permisos_rrhh')
    else:
        form = RevisionPermisoForm(instance=permiso)
    
    context = {
        'permiso': permiso,
        'form': form,
    }
    
    return render(request, 'core3/permisos/revisar.html', context)


# ========== GESTIÓN DE EMPLEADOS ==========
@login_required
@user_passes_test(es_rrhh)
def lista_empleados(request):
    """Lista todos los empleados"""
    busqueda = request.GET.get('buscar', '')
    filtro = request.GET.get('estado', 'todos')
    
    empleados = Empleado.objects.all().select_related('categoria', 'user')
    
    if busqueda:
        empleados = empleados.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(cedula__icontains=busqueda) |
            Q(correo__icontains=busqueda)
        )
    
    if filtro == 'activos':
        empleados = empleados.filter(activo=True)
    elif filtro == 'inactivos':
        empleados = empleados.filter(activo=False)
    
    empleados = empleados.order_by('-fecha_ingreso')
    
    context = {
        'empleados': empleados,
        'busqueda': busqueda,
        'filtro_actual': filtro,
    }
    
    return render(request, 'core3/empleados/lista.html', context)


@login_required
@user_passes_test(es_rrhh)
def detalle_empleado_rrhh(request, empleado_id):
    """Ver detalle completo de un empleado"""
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    # Obtener información relacionada
    nominas = empleado.nominas.all()[:10]
    permisos = empleado.permisos.all().order_by('-fecha_solicitud')[:10]
    
    context = {
        'empleado': empleado,
        'nominas': nominas,
        'permisos': permisos,
    }
    
    return render(request, 'core3/empleados/detalle.html', context)


@login_required
@user_passes_test(es_rrhh)
def editar_empleado_rrhh(request, empleado_id):
    """Editar información de un empleado"""
    from core2.forms import EmpleadoForm
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, f'Información de {empleado.nombre} actualizada.')
            return redirect('detalle_empleado_rrhh', empleado_id=empleado.id)
    else:
        form = EmpleadoForm(instance=empleado)
    
    context = {
        'empleado': empleado,
        'form': form,
    }
    
    return render(request, 'core3/empleados/editar.html', context)


@login_required
@user_passes_test(es_rrhh)
def desactivar_empleado(request, empleado_id):
    """Activar/Desactivar un empleado"""
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    if request.method == 'POST':
        empleado.activo = not empleado.activo
        empleado.save()
        
        estado = 'activado' if empleado.activo else 'desactivado'
        messages.success(request, f'Empleado {empleado.nombre} {estado}.')
        return redirect('detalle_empleado_rrhh', empleado_id=empleado.id)
    
    context = {'empleado': empleado}
    return render(request, 'core3/empleados/confirmar_desactivar.html', context)


# ========== GESTIÓN DE NÓMINAS ==========
@login_required
@user_passes_test(es_rrhh)
def lista_nominas_rrhh(request):
    """Lista todos los periodos de nómina"""
    periodos = PeriodoNomina.objects.all().order_by('-fecha_inicio')
    
    context = {'periodos': periodos}
    return render(request, 'core3/nominas/lista_periodos.html', context)


@login_required
@user_passes_test(es_rrhh)
def crear_periodo_nomina(request):
    """Crear un nuevo periodo de nómina"""
    if request.method == 'POST':
        form = PeriodoNominaForm(request.POST)
        if form.is_valid():
            periodo = form.save()
            messages.success(request, f'Periodo de nómina creado: {periodo}')
            return redirect('detalle_periodo_nomina', periodo_id=periodo.id)
    else:
        form = PeriodoNominaForm()
    
    context = {'form': form}
    return render(request, 'core3/nominas/crear_periodo.html', context)


@login_required
@user_passes_test(es_rrhh)
def detalle_periodo_nomina(request, periodo_id):
    """Ver detalle de un periodo de nómina"""
    periodo = get_object_or_404(PeriodoNomina, id=periodo_id)
    nominas = periodo.nominas.all().select_related('empleado')
    
    # Calcular totales
    total_devengado = nominas.aggregate(Sum('total_devengado'))['total_devengado__sum'] or 0
    total_deducciones = nominas.aggregate(Sum('total_deducciones'))['total_deducciones__sum'] or 0
    total_neto = nominas.aggregate(Sum('neto_pagar'))['neto_pagar__sum'] or 0
    
    context = {
        'periodo': periodo,
        'nominas': nominas,
        'total_devengado': total_devengado,
        'total_deducciones': total_deducciones,
        'total_neto': total_neto,
    }
    
    return render(request, 'core3/nominas/detalle_periodo.html', context)


@login_required
@user_passes_test(es_rrhh)
def generar_nominas(request, periodo_id):
    """Generar nóminas para todos los empleados activos en un periodo"""
    periodo = get_object_or_404(PeriodoNomina,id=periodo_id)
    
    if periodo.cerrado:
        messages.warning(request, 'Este periodo ya está cerrado.')
        return redirect('detalle_periodo_nomina', periodo_id=periodo.id)
    
    if request.method == 'POST':
        empleados_activos = Empleado.objects.filter(activo=True, categoria__isnull=False)
        nominas_creadas = 0
        nominas_existentes = 0
        
        # Obtener configuración de nómina
        config = ConfiguracionNomina.objects.filter(activo=True).first()
        
        for empleado in empleados_activos:
            # Verificar si ya existe una nómina para este empleado en este periodo
            nomina_existe = Nomina.objects.filter(empleado=empleado, periodo=periodo).exists()
            
            if nomina_existe:
                nominas_existentes += 1
                continue
            
            # Crear nómina
            salario_base = empleado.categoria.salario_base
            
            # Calcular deducciones básicas si hay configuración
            deducciones = Decimal('0.00')
            if config:
                deducciones = (
                    salario_base * (config.porcentaje_seguridad_social / 100) +
                    salario_base * (config.porcentaje_salud / 100) +
                    salario_base * (config.porcentaje_pension / 100)
                )
            
            nomina = Nomina.objects.create(
                empleado=empleado,
                periodo=periodo,
                salario_base=salario_base,
                deducciones=deducciones,
                bonificaciones=Decimal('0.00'),
                horas_extra=Decimal('0.00'),
                valor_hora_extra=Decimal('0.00'),
                total_devengado=salario_base,
                total_deducciones=deducciones,
                neto_pagar=salario_base - deducciones,
                pagado=False
            )
            
            nominas_creadas += 1
        
        messages.success(
            request,
            f'Nóminas generadas: {nominas_creadas} nuevas. '
            f'{nominas_existentes} ya existían.'
        )
        return redirect('detalle_periodo_nomina', periodo_id=periodo.id)
    
    # GET - Mostrar confirmación
    empleados_activos = Empleado.objects.filter(activo=True, categoria__isnull=False)
    nominas_existentes = Nomina.objects.filter(periodo=periodo).count()
    
    context = {
        'periodo': periodo,
        'empleados_activos': empleados_activos,
        'nominas_existentes': nominas_existentes,
    }
    
    return render(request, 'core3/nominas/generar_nominas.html', context)


@login_required
@user_passes_test(es_rrhh)
def editar_nomina(request, nomina_id):
    """Editar manualmente una nómina"""
    nomina = get_object_or_404(Nomina, id=nomina_id)
    
    if nomina.pagado:
        messages.warning(request, 'No se puede editar una nómina ya pagada.')
        return redirect('detalle_periodo_nomina', periodo_id=nomina.periodo.id)
    
    if request.method == 'POST':
        form = NominaManualForm(request.POST, instance=nomina)
        if form.is_valid():
            nomina = form.save(commit=False)
            nomina.calcular_totales()
            nomina.save()
            messages.success(request, 'Nómina actualizada correctamente.')
            return redirect('detalle_periodo_nomina', periodo_id=nomina.periodo.id)
    else:
        form = NominaManualForm(instance=nomina)
    
    # Obtener conceptos adicionales
    conceptos = nomina.conceptos.all()
    
    context = {
        'nomina': nomina,
        'form': form,
        'conceptos': conceptos,
    }
    
    return render(request, 'core3/nominas/editar_nomina.html', context)


@login_required
@user_passes_test(es_rrhh)
def agregar_concepto(request, nomina_id):
    """Agregar un concepto adicional a una nómina"""
    nomina = get_object_or_404(Nomina, id=nomina_id)
    
    if nomina.pagado:
        messages.warning(request, 'No se puede agregar conceptos a una nómina ya pagada.')
        return redirect('detalle_periodo_nomina', periodo_id=nomina.periodo.id)
    
    if request.method == 'POST':
        form = ConceptoNominaForm(request.POST)
        if form.is_valid():
            concepto = form.save(commit=False)
            concepto.nomina = nomina
            concepto.save()
            
            # Actualizar totales de la nómina
            if concepto.tipo == 'DEVENGADO':
                nomina.bonificaciones += concepto.valor
            else:
                nomina.deducciones += concepto.valor
            
            nomina.calcular_totales()
            nomina.save()
            
            messages.success(request, f'Concepto "{concepto.concepto}" agregado.')
            return redirect('editar_nomina', nomina_id=nomina.id)
    else:
        form = ConceptoNominaForm()
    
    context = {
        'nomina': nomina,
        'form': form,
    }
    
    return render(request, 'core3/nominas/agregar_concepto.html', context)


@login_required
@user_passes_test(es_rrhh)
def marcar_pagado(request, nomina_id):
    """Marcar una nómina como pagada"""
    nomina = get_object_or_404(Nomina, id=nomina_id)
    
    if request.method == 'POST':
        nomina.pagado = not nomina.pagado
        nomina.save()
        
        estado = 'pagada' if nomina.pagado else 'pendiente'
        messages.success(request, f'Nómina marcada como {estado}.')
        return redirect('detalle_periodo_nomina', periodo_id=nomina.periodo.id)
    
    context = {'nomina': nomina}
    return render(request, 'core3/nominas/confirmar_pago.html', context)


# ========== CONFIGURACIÓN ==========
@login_required
@user_passes_test(es_rrhh)
def configuracion_nomina(request):
    """Configurar parámetros generales de nómina"""
    config = ConfiguracionNomina.objects.filter(activo=True).first()
    
    if request.method == 'POST':
        if config:
            form = ConfiguracionNominaForm(request.POST, instance=config)
        else:
            form = ConfiguracionNominaForm(request.POST)
        
        if form.is_valid():
            # Desactivar configuraciones anteriores
            ConfiguracionNomina.objects.all().update(activo=False)
            
            # Guardar nueva configuración
            nueva_config = form.save(commit=False)
            nueva_config.activo = True
            nueva_config.save()
            
            messages.success(request, 'Configuración de nómina actualizada.')
            return redirect('configuracion_nomina')
    else:
        form = ConfiguracionNominaForm(instance=config) if config else ConfiguracionNominaForm()
    
    context = {
        'form': form,
        'config': config,
    }
    
    return render(request, 'core3/configuracion/nomina.html', context)


# ========== REPORTES ==========
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from datetime import date

@login_required
@user_passes_test(es_rrhh)
def reportes_rrhh(request):
    """Dashboard de reportes y estadísticas"""

    # ===== Empleados =====
    total_empleados = Empleado.objects.count()
    empleados_activos = Empleado.objects.filter(activo=True).count()
    empleados_inactivos = total_empleados - empleados_activos

    # ===== Solicitudes =====
    total_solicitudes = Solicitud.objects.count()
    solicitudes_pendientes = Solicitud.objects.filter(estado__nombre='Pendiente').count()
    solicitudes_aprobadas = Solicitud.objects.filter(estado__nombre='Aprobado').count()
    solicitudes_rechazadas = Solicitud.objects.filter(estado__nombre='Rechazado').count()

    if total_solicitudes > 0:
        porcentaje_solicitudes_pendientes = round((solicitudes_pendientes / total_solicitudes) * 100, 2)
        porcentaje_solicitudes_aprobadas = round((solicitudes_aprobadas / total_solicitudes) * 100, 2)
        porcentaje_solicitudes_rechazadas = round((solicitudes_rechazadas / total_solicitudes) * 100, 2)
    else:
        porcentaje_solicitudes_pendientes = porcentaje_solicitudes_aprobadas = porcentaje_solicitudes_rechazadas = 0

    # ===== Permisos =====
    total_permisos = Permiso.objects.count()
    permisos_pendientes = Permiso.objects.filter(estado='PENDIENTE').count()
    permisos_aprobados = Permiso.objects.filter(estado='APROBADO').count()
    permisos_rechazados = Permiso.objects.filter(estado='RECHAZADO').count()

    if total_permisos > 0:
        porcentaje_permisos_pendientes = round((permisos_pendientes / total_permisos) * 100, 2)
        porcentaje_permisos_aprobados = round((permisos_aprobados / total_permisos) * 100, 2)
        porcentaje_permisos_rechazados = round((permisos_rechazados / total_permisos) * 100, 2)
    else:
        porcentaje_permisos_pendientes = porcentaje_permisos_aprobados = porcentaje_permisos_rechazados = 0

    # ===== Nóminas =====
    total_nominas = Nomina.objects.count()
    nominas_pagadas = Nomina.objects.filter(pagado=True).count()
    nominas_pendientes = total_nominas - nominas_pagadas

    if total_nominas > 0:
        porcentaje_nominas_pagadas = round((nominas_pagadas / total_nominas) * 100, 2)
        porcentaje_nominas_pendientes = round((nominas_pendientes / total_nominas) * 100, 2)
    else:
        porcentaje_nominas_pagadas = porcentaje_nominas_pendientes = 0

    # ===== Últimos registros =====
    solicitudes_contratadas = ProcesoContratacion.objects.filter(
        estado_proceso='CONTRATADO'
    ).values_list('solicitud_id', flat=True)

    ultimas_solicitudes = Solicitud.objects.exclude(
        id__in=solicitudes_contratadas
    ).order_by('-fecha_creacion')[:5]

    ultimos_permisos = Permiso.objects.all().order_by('-fecha_solicitud')[:5]

    # ===== Distribución por categoría =====
    empleados_por_categoria = Empleado.objects.filter(activo=True).values(
        'categoria__nombre'
    ).annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')

    # ===== Nómina total del mes actual =====
    mes_actual = date.today().month
    ano_actual = date.today().year

    nominas_mes = Nomina.objects.filter(
        periodo__fecha_inicio__month=mes_actual,
        periodo__fecha_inicio__year=ano_actual
    )
    total_nomina_mes = nominas_mes.aggregate(Sum('neto_pagar'))['neto_pagar__sum'] or 0

    # ===== Contexto =====
    context = {
        # Empleados
        'total_empleados': total_empleados,
        'empleados_activos': empleados_activos,
        'empleados_inactivos': empleados_inactivos,

        # Solicitudes
        'total_solicitudes': total_solicitudes,
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aprobadas': solicitudes_aprobadas,
        'solicitudes_rechazadas': solicitudes_rechazadas,
        'porcentaje_solicitudes_pendientes': porcentaje_solicitudes_pendientes,
        'porcentaje_solicitudes_aprobadas': porcentaje_solicitudes_aprobadas,
        'porcentaje_solicitudes_rechazadas': porcentaje_solicitudes_rechazadas,

        # Permisos
        'total_permisos': total_permisos,
        'permisos_pendientes': permisos_pendientes,
        'permisos_aprobados': permisos_aprobados,
        'permisos_rechazados': permisos_rechazados,
        'porcentaje_permisos_pendientes': porcentaje_permisos_pendientes,
        'porcentaje_permisos_aprobados': porcentaje_permisos_aprobados,
        'porcentaje_permisos_rechazados': porcentaje_permisos_rechazados,

        # Nóminas
        'total_nominas': total_nominas,
        'nominas_pagadas': nominas_pagadas,
        'nominas_pendientes': nominas_pendientes,
        'porcentaje_nominas_pagadas': porcentaje_nominas_pagadas,
        'porcentaje_nominas_pendientes': porcentaje_nominas_pendientes,

        # Otros
        'empleados_por_categoria': empleados_por_categoria,
        'total_nomina_mes': total_nomina_mes,
        'ultimas_solicitudes': ultimas_solicitudes,
        'ultimos_permisos': ultimos_permisos,
    }

    return render(request, 'core3/reportes/dashboard.html', context)
