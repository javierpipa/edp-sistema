from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from proyectos.models import Proyecto, CuadroControl
from actividades.models import Actividad
from noc.models import NoConformidad
from empresas.models import Empresa
from users.models import User


def dashboard(request):
    proyectos = Proyecto.objects.all().select_related('control')
    total_proyectos = proyectos.count()
    proyectos_finalizados = proyectos.filter(estado='finalizado').count()
    proyectos_activos = proyectos.filter(estado='en_ejecucion').count()

    actividades = Actividad.objects.all()
    total_actividades = actividades.count()
    completadas = actividades.filter(estado='completada').count()
    avance_promedio = actividades.aggregate(Avg('avance'))['avance__avg'] or 0

    noc_abiertas = NoConformidad.objects.filter(estado='abierta').count()
    noc_proceso = NoConformidad.objects.filter(estado='en_proceso').count()
    noc_cerradas = NoConformidad.objects.filter(estado='cerrada').count()

    data_chart = {
        "labels": [p.codigo for p in proyectos],
        "values": [float(p.control.avance_global) if hasattr(p, 'control') else 0 for p in proyectos],
    }

    context = {
        "total_proyectos": total_proyectos,
        "proyectos_activos": proyectos_activos,
        "proyectos_finalizados": proyectos_finalizados,
        "total_actividades": total_actividades,
        "completadas": completadas,
        "avance_promedio": round(avance_promedio, 2),
        "noc_abiertas": noc_abiertas,
        "noc_proceso": noc_proceso,
        "noc_cerradas": noc_cerradas,
        "chart": data_chart,
    }
    return render(request, "dashboard/dashboard.html", context)


def proyectos_lista(request):
    """Lista de todos los proyectos con filtros"""
    estado_filter = request.GET.get('estado', '')
    search = request.GET.get('search', '')
    
    proyectos = Proyecto.objects.all().select_related('cliente', 'responsable', 'control')
    
    # Filtros
    if estado_filter:
        proyectos = proyectos.filter(estado=estado_filter)
    
    if search:
        proyectos = proyectos.filter(
            Q(codigo__icontains=search) | 
            Q(nombre__icontains=search) |
            Q(cliente__nombre__icontains=search)
        )
    
    # Agregar estadísticas por proyecto
    proyectos_data = []
    for proyecto in proyectos:
        total_act = proyecto.actividades.count()
        completadas = proyecto.actividades.filter(estado='completada').count()
        total_noc = proyecto.noc.count()
        noc_abiertas = proyecto.noc.filter(estado='abierta').count()
        avance = proyecto.control.avance_global if hasattr(proyecto, 'control') else 0
        
        proyectos_data.append({
            'proyecto': proyecto,
            'total_actividades': total_act,
            'actividades_completadas': completadas,
            'total_noc': total_noc,
            'noc_abiertas': noc_abiertas,
            'avance_global': avance,
        })
    
    context = {
        'proyectos_data': proyectos_data,
        'estado_filter': estado_filter,
        'search': search,
        'estados': Proyecto.ESTADO_CHOICES,
    }
    return render(request, "dashboard/proyectos_lista.html", context)


def proyecto_detalle(request, proyecto_id):
    """Detalle completo de un proyecto"""
    proyecto = get_object_or_404(
        Proyecto.objects.select_related('cliente', 'responsable', 'control'),
        id=proyecto_id
    )
    
    # Actividades del proyecto
    actividades = proyecto.actividades.all().select_related('responsable').order_by('-fecha_programada')
    
    # Estadísticas de actividades
    total_actividades = actividades.count()
    act_completadas = actividades.filter(estado='completada').count()
    act_en_ejecucion = actividades.filter(estado='en_ejecucion').count()
    act_pendientes = actividades.filter(estado='pendiente').count()
    act_atrasadas = actividades.filter(estado='atrasada').count()
    
    # No conformidades
    nocs = proyecto.noc.all().select_related('responsable').order_by('-fecha_detectada')
    total_noc = nocs.count()
    noc_abiertas = nocs.filter(estado='abierta').count()
    noc_proceso = nocs.filter(estado='en_proceso').count()
    noc_cerradas = nocs.filter(estado='cerrada').count()
    
    # Gráfico de actividades por estado
    chart_actividades = {
        'labels': ['Completadas', 'En Ejecución', 'Pendientes', 'Atrasadas'],
        'values': [act_completadas, act_en_ejecucion, act_pendientes, act_atrasadas],
        'colors': ['#28a745', '#007bff', '#ffc107', '#dc3545']
    }
    
    # Gráfico de NOC por estado
    chart_noc = {
        'labels': ['Abiertas', 'En Proceso', 'Cerradas'],
        'values': [noc_abiertas, noc_proceso, noc_cerradas],
        'colors': ['#dc3545', '#ffc107', '#28a745']
    }
    
    context = {
        'proyecto': proyecto,
        'actividades': actividades[:20],  # Últimas 20 actividades
        'total_actividades': total_actividades,
        'act_completadas': act_completadas,
        'act_en_ejecucion': act_en_ejecucion,
        'act_pendientes': act_pendientes,
        'act_atrasadas': act_atrasadas,
        'nocs': nocs[:10],  # Últimas 10 NOC
        'total_noc': total_noc,
        'noc_abiertas': noc_abiertas,
        'noc_proceso': noc_proceso,
        'noc_cerradas': noc_cerradas,
        'chart_actividades': chart_actividades,
        'chart_noc': chart_noc,
    }
    return render(request, "dashboard/proyecto_detalle.html", context)


def actividades_lista(request):
    """Lista de todas las actividades con filtros y paginación"""
    from django.core.paginator import Paginator
    
    # Filtros
    estado_filter = request.GET.get('estado', '')
    proyecto_filter = request.GET.get('proyecto', '')
    search = request.GET.get('search', '')
    
    # Query base
    actividades = Actividad.objects.all().select_related('proyecto', 'responsable').order_by('-fecha_programada')
    
    # Aplicar filtros
    if estado_filter:
        actividades = actividades.filter(estado=estado_filter)
    
    if proyecto_filter:
        actividades = actividades.filter(proyecto_id=proyecto_filter)
    
    if search:
        actividades = actividades.filter(
            Q(item__icontains=search) | 
            Q(descripcion__icontains=search) |
            Q(proyecto__codigo__icontains=search)
        )
    
    # Estadísticas generales
    total_actividades = Actividad.objects.count()
    completadas = Actividad.objects.filter(estado='completada').count()
    en_ejecucion = Actividad.objects.filter(estado='en_ejecucion').count()
    pendientes = Actividad.objects.filter(estado='pendiente').count()
    atrasadas = Actividad.objects.filter(estado='atrasada').count()
    avance_promedio = Actividad.objects.aggregate(Avg('avance'))['avance__avg'] or 0
    
    # Estadísticas filtradas
    total_filtradas = actividades.count()
    
    # Paginación
    paginator = Paginator(actividades, 20)  # 20 actividades por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Proyectos para el filtro
    proyectos = Proyecto.objects.all().order_by('codigo')
    
    # Gráfico de actividades por estado
    chart_data = {
        'labels': ['Completadas', 'En Ejecución', 'Pendientes', 'Atrasadas'],
        'values': [completadas, en_ejecucion, pendientes, atrasadas],
        'colors': ['#28a745', '#007bff', '#ffc107', '#dc3545']
    }
    
    context = {
        'page_obj': page_obj,
        'total_actividades': total_actividades,
        'completadas': completadas,
        'en_ejecucion': en_ejecucion,
        'pendientes': pendientes,
        'atrasadas': atrasadas,
        'avance_promedio': round(avance_promedio, 2),
        'total_filtradas': total_filtradas,
        'estado_filter': estado_filter,
        'proyecto_filter': proyecto_filter,
        'search': search,
        'estados': Actividad.ESTADO_CHOICES,
        'proyectos': proyectos,
        'chart_data': chart_data,
    }
    return render(request, "dashboard/actividades_lista.html", context)


# ==================== CRUD PROYECTOS ====================

def proyecto_crear(request):
    """Crear nuevo proyecto"""
    if request.method == 'POST':
        try:
            proyecto = Proyecto.objects.create(
                codigo=request.POST['codigo'],
                nombre=request.POST['nombre'],
                cliente_id=request.POST['cliente'],
                responsable_id=request.POST['responsable'],
                supervisor=request.POST.get('supervisor', ''),
                fecha_inicio=request.POST['fecha_inicio'],
                fecha_termino=request.POST.get('fecha_termino') or None,
                estado=request.POST['estado']
            )
            # Crear cuadro de control
            CuadroControl.objects.create(proyecto=proyecto)
            messages.success(request, f'Proyecto {proyecto.codigo} creado exitosamente.')
            return redirect('dashboard:proyecto_detalle', proyecto_id=proyecto.id)
        except Exception as e:
            messages.error(request, f'Error al crear proyecto: {e}')
    
    empresas = Empresa.objects.all()
    usuarios = User.objects.filter(is_active=True)
    context = {
        'empresas': empresas,
        'usuarios': usuarios,
        'estados': Proyecto.ESTADO_CHOICES,
    }
    return render(request, 'dashboard/proyecto_form.html', context)


def proyecto_editar(request, proyecto_id):
    """Editar proyecto existente"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        try:
            proyecto.codigo = request.POST['codigo']
            proyecto.nombre = request.POST['nombre']
            proyecto.cliente_id = request.POST['cliente']
            proyecto.responsable_id = request.POST['responsable']
            proyecto.supervisor = request.POST.get('supervisor', '')
            proyecto.fecha_inicio = request.POST['fecha_inicio']
            proyecto.fecha_termino = request.POST.get('fecha_termino') or None
            proyecto.estado = request.POST['estado']
            proyecto.save()
            messages.success(request, f'Proyecto {proyecto.codigo} actualizado exitosamente.')
            return redirect('dashboard:proyecto_detalle', proyecto_id=proyecto.id)
        except Exception as e:
            messages.error(request, f'Error al actualizar proyecto: {e}')
    
    empresas = Empresa.objects.all()
    usuarios = User.objects.filter(is_active=True)
    context = {
        'proyecto': proyecto,
        'empresas': empresas,
        'usuarios': usuarios,
        'estados': Proyecto.ESTADO_CHOICES,
    }
    return render(request, 'dashboard/proyecto_form.html', context)


def proyecto_eliminar(request, proyecto_id):
    """Eliminar proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        codigo = proyecto.codigo
        proyecto.delete()
        messages.success(request, f'Proyecto {codigo} eliminado exitosamente.')
        return redirect('dashboard:proyectos_lista')
    
    context = {'proyecto': proyecto}
    return render(request, 'dashboard/proyecto_confirm_delete.html', context)


# ==================== CRUD ACTIVIDADES ====================

def actividad_crear(request, proyecto_id=None):
    """Crear nueva actividad"""
    if request.method == 'POST':
        try:
            actividad = Actividad.objects.create(
                proyecto_id=request.POST['proyecto'],
                item=request.POST.get('item', ''),
                descripcion=request.POST['descripcion'],
                responsable_id=request.POST.get('responsable') or None,
                fecha_programada=request.POST.get('fecha_programada') or None,
                fecha_real=request.POST.get('fecha_real') or None,
                avance=request.POST.get('avance', 0),
                estado=request.POST['estado'],
                observaciones=request.POST.get('observaciones', '')
            )
            # Actualizar cuadro de control
            if hasattr(actividad.proyecto, 'control'):
                actividad.proyecto.control.actualizar()
            
            messages.success(request, 'Actividad creada exitosamente.')
            return redirect('dashboard:proyecto_detalle', proyecto_id=actividad.proyecto.id)
        except Exception as e:
            messages.error(request, f'Error al crear actividad: {e}')
    
    proyectos = Proyecto.objects.all()
    usuarios = User.objects.filter(is_active=True)
    proyecto_seleccionado = None
    if proyecto_id:
        proyecto_seleccionado = get_object_or_404(Proyecto, id=proyecto_id)
    
    context = {
        'proyectos': proyectos,
        'usuarios': usuarios,
        'estados': Actividad.ESTADO_CHOICES,
        'proyecto_seleccionado': proyecto_seleccionado,
    }
    return render(request, 'dashboard/actividad_form.html', context)


def actividad_editar(request, actividad_id):
    """Editar actividad existente"""
    actividad = get_object_or_404(Actividad, id=actividad_id)
    
    if request.method == 'POST':
        try:
            actividad.proyecto_id = request.POST['proyecto']
            actividad.item = request.POST.get('item', '')
            actividad.descripcion = request.POST['descripcion']
            actividad.responsable_id = request.POST.get('responsable') or None
            actividad.fecha_programada = request.POST.get('fecha_programada') or None
            actividad.fecha_real = request.POST.get('fecha_real') or None
            actividad.avance = request.POST.get('avance', 0)
            actividad.estado = request.POST['estado']
            actividad.observaciones = request.POST.get('observaciones', '')
            actividad.save()
            
            # Actualizar cuadro de control
            if hasattr(actividad.proyecto, 'control'):
                actividad.proyecto.control.actualizar()
            
            messages.success(request, 'Actividad actualizada exitosamente.')
            return redirect('dashboard:proyecto_detalle', proyecto_id=actividad.proyecto.id)
        except Exception as e:
            messages.error(request, f'Error al actualizar actividad: {e}')
    
    proyectos = Proyecto.objects.all()
    usuarios = User.objects.filter(is_active=True)
    context = {
        'actividad': actividad,
        'proyectos': proyectos,
        'usuarios': usuarios,
        'estados': Actividad.ESTADO_CHOICES,
    }
    return render(request, 'dashboard/actividad_form.html', context)


def actividad_eliminar(request, actividad_id):
    """Eliminar actividad"""
    actividad = get_object_or_404(Actividad, id=actividad_id)
    proyecto_id = actividad.proyecto.id
    
    if request.method == 'POST':
        actividad.delete()
        # Actualizar cuadro de control
        proyecto = Proyecto.objects.get(id=proyecto_id)
        if hasattr(proyecto, 'control'):
            proyecto.control.actualizar()
        
        messages.success(request, 'Actividad eliminada exitosamente.')
        return redirect('dashboard:proyecto_detalle', proyecto_id=proyecto_id)
    
    context = {'actividad': actividad}
    return render(request, 'dashboard/actividad_confirm_delete.html', context)


# ==================== CRUD EMPRESAS ====================

def empresa_crear(request):
    """Crear nueva empresa"""
    if request.method == 'POST':
        try:
            empresa = Empresa.objects.create(
                nombre=request.POST['nombre'],
                rut=request.POST.get('rut', ''),
                contacto=request.POST.get('contacto', ''),
                correo=request.POST.get('correo', '')
            )
            messages.success(request, f'Empresa {empresa.nombre} creada exitosamente.')
            return redirect('dashboard:empresas_lista')
        except Exception as e:
            messages.error(request, f'Error al crear empresa: {e}')
    
    return render(request, 'dashboard/empresa_form.html')


def empresa_editar(request, empresa_id):
    """Editar empresa existente"""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        try:
            empresa.nombre = request.POST['nombre']
            empresa.rut = request.POST.get('rut', '')
            empresa.contacto = request.POST.get('contacto', '')
            empresa.correo = request.POST.get('correo', '')
            empresa.save()
            messages.success(request, f'Empresa {empresa.nombre} actualizada exitosamente.')
            return redirect('dashboard:empresas_lista')
        except Exception as e:
            messages.error(request, f'Error al actualizar empresa: {e}')
    
    context = {'empresa': empresa}
    return render(request, 'dashboard/empresa_form.html', context)


def empresa_eliminar(request, empresa_id):
    """Eliminar empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        nombre = empresa.nombre
        empresa.delete()
        messages.success(request, f'Empresa {nombre} eliminada exitosamente.')
        return redirect('dashboard:empresas_lista')
    
    context = {'empresa': empresa}
    return render(request, 'dashboard/empresa_confirm_delete.html', context)


def empresas_lista(request):
    """Lista de empresas"""
    search = request.GET.get('search', '')
    empresas = Empresa.objects.all()
    
    if search:
        empresas = empresas.filter(
            Q(nombre__icontains=search) | 
            Q(rut__icontains=search)
        )
    
    # Agregar conteo de proyectos por empresa
    empresas_data = []
    for empresa in empresas:
        empresas_data.append({
            'empresa': empresa,
            'total_proyectos': empresa.proyectos.count(),
            'proyectos_activos': empresa.proyectos.filter(estado='en_ejecucion').count(),
        })
    
    context = {
        'empresas_data': empresas_data,
        'search': search,
    }
    return render(request, 'dashboard/empresas_lista.html', context)


# ==================== CRUD NOC ====================

def noc_crear(request, proyecto_id=None):
    """Crear nueva no conformidad"""
    if request.method == 'POST':
        try:
            noc = NoConformidad.objects.create(
                proyecto_id=request.POST['proyecto'],
                codigo=request.POST['codigo'],
                descripcion=request.POST['descripcion'],
                responsable_id=request.POST.get('responsable') or None,
                fecha_detectada=request.POST['fecha_detectada'],
                fecha_cierre=request.POST.get('fecha_cierre') or None,
                estado=request.POST['estado'],
                accion_correctiva=request.POST.get('accion_correctiva', '')
            )
            messages.success(request, f'NOC {noc.codigo} creada exitosamente.')
            return redirect('dashboard:proyecto_detalle', proyecto_id=noc.proyecto.id)
        except Exception as e:
            messages.error(request, f'Error al crear NOC: {e}')
    
    proyectos = Proyecto.objects.all()
    usuarios = User.objects.filter(is_active=True)
    proyecto_seleccionado = None
    if proyecto_id:
        proyecto_seleccionado = get_object_or_404(Proyecto, id=proyecto_id)
    
    context = {
        'proyectos': proyectos,
        'usuarios': usuarios,
        'estados': NoConformidad.ESTADO_CHOICES,
        'proyecto_seleccionado': proyecto_seleccionado,
    }
    return render(request, 'dashboard/noc_form.html', context)


def noc_editar(request, noc_id):
    """Editar no conformidad existente"""
    noc = get_object_or_404(NoConformidad, id=noc_id)
    
    if request.method == 'POST':
        try:
            noc.proyecto_id = request.POST['proyecto']
            noc.codigo = request.POST['codigo']
            noc.descripcion = request.POST['descripcion']
            noc.responsable_id = request.POST.get('responsable') or None
            noc.fecha_detectada = request.POST['fecha_detectada']
            noc.fecha_cierre = request.POST.get('fecha_cierre') or None
            noc.estado = request.POST['estado']
            noc.accion_correctiva = request.POST.get('accion_correctiva', '')
            noc.save()
            messages.success(request, f'NOC {noc.codigo} actualizada exitosamente.')
            return redirect('dashboard:proyecto_detalle', proyecto_id=noc.proyecto.id)
        except Exception as e:
            messages.error(request, f'Error al actualizar NOC: {e}')
    
    proyectos = Proyecto.objects.all()
    usuarios = User.objects.filter(is_active=True)
    context = {
        'noc': noc,
        'proyectos': proyectos,
        'usuarios': usuarios,
        'estados': NoConformidad.ESTADO_CHOICES,
    }
    return render(request, 'dashboard/noc_form.html', context)


def noc_eliminar(request, noc_id):
    """Eliminar no conformidad"""
    noc = get_object_or_404(NoConformidad, id=noc_id)
    proyecto_id = noc.proyecto.id
    
    if request.method == 'POST':
        codigo = noc.codigo
        noc.delete()
        messages.success(request, f'NOC {codigo} eliminada exitosamente.')
        return redirect('dashboard:proyecto_detalle', proyecto_id=proyecto_id)
    
    context = {'noc': noc}
    return render(request, 'dashboard/noc_confirm_delete.html', context)
