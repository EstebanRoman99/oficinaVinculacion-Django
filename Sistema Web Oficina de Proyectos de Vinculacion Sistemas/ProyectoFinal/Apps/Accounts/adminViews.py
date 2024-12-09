from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views.decorators.cache import cache_control
from django.http import FileResponse, HttpResponse
from django.db.models import Value, F
from django.db.models.functions import Concat

from io import BytesIO
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings

import io
import xlwt
import ast

# Import model
#from .recommend_doc import recomendaciones_docentes
from .recomendacion_d import recomendaciones_docentes

#from django.db.models import Count
from datetime import date, timedelta, datetime
from django.db.models.functions import Substr
import math
from .models import *
from .forms import *
from .adminForms import *
from .decorators import *
from .utils import enviar_email
from .views import generarCodigo, obtenerCodigo, buscarCodigo
# Create your views here.

import pandas as pd
import csv

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def anteproyectos(request, page, orderB, filter):
    group = request.user.groups.all()[0].name    
    all_anteproyectos = Anteproyecto.objects.all()     
    start = (page-1)*10    
    end = page*10        
    
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_anteproyectos = buscar_anteproyecto(all_anteproyectos, text, opc)                        
            anteproyectos = all_anteproyectos
            start = 0
            end = anteproyectos.count()
            totalA = all_anteproyectos.count()                        
            search = '.'             
            context = {'group': group, 'anteproyectos': anteproyectos, 'totalA': totalA, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'filter': filter, 'title': 'Anteproyectos'}
            return render(request, 'Admin/anteproyectos.html', context)    
    
    all_anteproyectos = filtrar_anteproyectos(all_anteproyectos, filter)
    all_anteproyectos = ordenar_anteproyectos(all_anteproyectos, orderB)        
    anteproyectos = all_anteproyectos[start:end]
    if end != anteproyectos.count():
        end = end-10+anteproyectos.count()
    totalA = all_anteproyectos.count()
    n_buttons = math.ceil(totalA/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    context = {'group': group, 'anteproyectos': anteproyectos, 'totalA': totalA, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'orderB': orderB, 'filter': filter, 'title': 'Anteproyectos'}
    return render(request, 'Admin/anteproyectos.html', context)    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def residencias(request, page, orderB, filter):
    group = request.user.groups.all()[0].name   
    all_residencias = Residencia.objects.all()             
    start = (page-1)*10    
    end = page*10
    
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_residencias = buscar_residencia(all_residencias, text, opc)
            residencias = all_residencias
            start = 0
            end = residencias.count()
            totalR = all_residencias.count()                        
            search = '.'                         
            context = {'group': group, 'residencias': residencias, 'totalR': totalR, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'filter': filter, 'title': 'Residencias'}
            return render(request, 'Admin/residencias.html', context)            
        
    all_residencias = filtrar_residencias(all_residencias, filter)
    all_residencias = ordenar_residencias(all_residencias, orderB)
    residencias = all_residencias[start:end]
    if end != residencias.count():
        end = end-10+residencias.count()
    totalR = all_residencias.count()
    n_buttons = math.ceil(totalR/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    
    context = {'group': group, 'residencias': residencias, 'totalR': totalR, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'orderB': orderB, 'filter': filter, 'title': 'Residencias'}
    return render(request, 'Admin/residencias.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def expedientes(request, page, orderB, filter):
    group = request.user.groups.all()[0].name      
    all_estudiantes = Estudiante.objects.all().exclude(expediente=None)  
    start = (page-1)*10    
    end = page*10    
    
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:                        
            all_estudiantes = buscar_estudiante(all_estudiantes, text, opc)            
            estudiantes = all_estudiantes
            start = 0
            end = estudiantes.count()
            totalE = all_estudiantes.count()            
            asesorI = '.'    
            search = '.'             
            context = {'group': group, 'estudiantes': estudiantes, 'totalE': totalE, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'filter': filter, 'title': 'Expedientes'}
            return render(request, 'Admin/expedientes.html', context)   
            
    all_estudiantes = filtrar_expedientes(all_estudiantes, filter)
    all_estudiantes = ordenar_estudiantes(all_estudiantes, orderB)
    estudiantes = all_estudiantes[start:end]
    if end != estudiantes.count():
        end = end-10+estudiantes.count()
    totalE = all_estudiantes.count()
    n_buttons = math.ceil(totalE/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    context = {'group': group, 'estudiantes': estudiantes, 'totalE': totalE, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'orderB': orderB, 'filter': filter, 'title': 'Expedientes'}
    return render(request, 'Admin/expedientes.html', context)   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def verExpediente(request, pk):
    data = ['id_dictamen', 'id_solicitudResidencia', 'id_anteproyecto', 'id_horario', 'id_cartaAceptacion', 'id_cartaCompromiso', 'id_cronograma', 'id_cartaPresentacion']    
    group = request.user.groups.all()[0].name
    estudiante = Estudiante.objects.get(id = pk)
    expediente = estudiante.expediente
    r1 = expediente.reporteParcial1
    r2 = expediente.reporteParcial2
    rF = expediente.reporteFinal                
    formE = ExpedienteForm(instance=expediente)
    form1 = Reporte1Form(instance = r1)                  
    form2 = Reporte2Form(instance = r2)                  
    formF = ReporteFinalForm(instance = rF)                      
    formEstado = ExpedienteEstadoForm(instance = expediente)        
    
    if request.method == 'POST':
        formEstado = ExpedienteEstadoForm(request.POST, instance = expediente)     
        if formEstado.is_valid():
            formEstado.save()  
            enviar_email('Expediente FINALIZADO', '', [estudiante.correoElectronico], 4, 'FINALIZADO')
            estado = formEstado.cleaned_data.get("estatus") 
            if estado == 'FINALIZADO':
                descripcion = '<hr /><p><strong><span style="color:#e74c3c"><big>Feliciades!!!! </big></span></strong></p><hr /><div><p style="margin-left:0px; margin-right:0px"><span style="color:#3498db"><em>Tu expediente ha sido revisado y se ha dado por finalizado. Ya puedes pasar a la oficina del departamento de vinculaci&oacute;n a recoger tu documento.</em></span></p><br/><div style="width:100%"><div style="height:0;padding-bottom:56.25%;position:relative;width:100%"><iframe allowfullscreen="" frameBorder="0" height="100%" src="https://giphy.com/embed/G96zgIcQn1L2xpmdxi/video" style="left:0;position:absolute;top:0" width="100%"></iframe></div></div>'
                Avisos.objects.create(entidad = 'PRIVADO', tiempoVida = 7, descripcion = descripcion, estudiante = estudiante)
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
    context = {'group': group, 'data': data, 'estudiante': estudiante, 'expediente': expediente, 'r1': r1, 'r2': r2, 'rF': rF, 'formE': formE, 'form1': form1, 'form2': form2, 'formF': formF, 'formEstado': formEstado, 'title': 'Expediente'}
    return render(request, 'Admin/verExpediente.html', context)             

@admin_only
def eliminarExpediente(request, pk):
    expediente = Expediente.objects.get(id = pk)
    expediente.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def estudiantes(request, page, orderB):
    group = request.user.groups.all()[0].name    
    all_estudiantes = Estudiante.objects.all()  
    all_e_anteproyectos = Estudiante_Anteproyecto.objects.filter(estado = 'ACTIVO')           
    all_e_residencias = Estudiante_Residencia.objects.filter(estado = 'ACTIVO')       
    start = (page-1)*10    
    end = page*10            
    
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search']                         
        if text:
            all_estudiantes = buscar_estudiante(all_estudiantes, text, opc)            
            estudiantes = all_estudiantes
            
            for i in estudiantes:
                anteproyecto_e = all_e_anteproyectos.filter(estudiante = i)
                residencia_e = all_e_residencias.filter(estudiante = i)        

                if anteproyecto_e:
                    estado_anteproyecto = anteproyecto_e[0].anteproyecto.estatus
                else:
                    estado_anteproyecto = None

                if residencia_e:
                    estado_residencia = residencia_e[0].residencia.estatus
                else:
                    estado_residencia = None

                setattr(i, 'anteproyecto_estatus', estado_anteproyecto)  
                setattr(i, 'residencia_estatus', estado_residencia)          
        
            start = 0
            end = estudiantes.count()
            totalE = all_estudiantes.count()            
            asesorI = '.'    
            search = '.'             
            context = {'group': group, 'estudiantes': estudiantes, 'totalE': totalE, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'title': 'Estudiantes'}
            return render(request, 'Admin/estudiantes.html', context)   
                
    all_estudiantes = ordenar_estudiantes(all_estudiantes, orderB)
    estudiantes = all_estudiantes[start:end]
    
    for i in estudiantes:
        anteproyecto_e = all_e_anteproyectos.filter(estudiante = i)
        residencia_e = all_e_residencias.filter(estudiante = i)        
        
        if anteproyecto_e:
            estado_anteproyecto = anteproyecto_e[0].anteproyecto.estatus
        else:
            estado_anteproyecto = None
            
        if residencia_e:
            estado_residencia = residencia_e[0].residencia.estatus
        else:
            estado_residencia = None
                    
        setattr(i, 'anteproyecto_estatus', estado_anteproyecto)  
        setattr(i, 'residencia_estatus', estado_residencia)          
        
    
    if end != estudiantes.count():
        end = end-10+estudiantes.count()
    totalE = all_estudiantes.count()
    n_buttons = math.ceil(totalE/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    context = {'group': group, 'estudiantes': estudiantes, 'totalE': totalE, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'orderB': orderB, 'title': 'Estudiantes'}
    return render(request, 'Admin/estudiantes.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def docentes(request, page, orderB):
    group = request.user.groups.all()[0].name    
    all_docentes = Docente.objects.all()
    start = (page-1)*10    
    end = page*10                    
        
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_docentes = buscar_docente(all_docentes, text, opc)                                                                                            
            docentes = all_docentes
            start = 0
            end = docentes.count()
            totalD = all_docentes.count()                        
            search = '.'      
            context = {'group': group, 'docentes': docentes, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'title': 'Docentes'}
            return render(request, 'Admin/docentes.html', context)            
            
    all_docentes = ordenar_docentes(all_docentes, orderB)
    docentes = all_docentes[start:end]    
    if end != docentes.count():
        end = end-10+docentes.count()
    totalD = all_docentes.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    context = {'group': group, 'docentes': docentes, 'totalD': totalD, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'orderB': orderB, 'title': 'Docentes'}
    return render(request, 'Admin/docentes.html', context)     

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@publicView
def verAnteproyecto(request, pk):
    group = request.user.groups.all()[0].name    
    anteproyecto = Anteproyecto.objects.get(id = pk)    
    all_estudiantes = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto)            
    all_anteproyectos = Estudiante_Anteproyecto.objects.all()            
    estudiantes = [i.estudiante for i in all_estudiantes ]            
    historial_estudiantes = []  
    all_estudiantes_a = all_estudiantes.filter(estado = 'ACTIVO')              
    lista_correos = [i.estudiante.correoElectronico for i in all_estudiantes_a ]
    resi = None
    
    for i in estudiantes:        
        anteproyecto_e = all_estudiantes.filter(estudiante = i)                
        all_anteproyectos_e = all_anteproyectos.filter(estudiante = i).count()
        if all_anteproyectos_e > 1: historial_estudiantes.append(i)                
        
        if anteproyecto_e:
            estado_anteproyecto = anteproyecto_e[0].estado
        else:
            estado_anteproyecto = None                    
                    
        setattr(i, 'anteproyecto_estatus', estado_anteproyecto)                  
    
    actualizaciones = Actualizacion_anteproyecto.objects.filter(anteproyecto = anteproyecto).order_by('-fecha')
    revisor1 = anteproyecto.revisor1 
    revisor2 = anteproyecto.revisor2                
    dependencia = anteproyecto.dependencia 
    observacion = anteproyecto.observacion
    estadoInicial = anteproyecto.estatus
    fechaObservacion = None
    observaciones = None
    dias = 0
    fechaObservacion = None
    fechaCorte = None
    fechaActual = date.today
    fechaObservacion = None
    data = ['id_mision', 'id_codigoUnion', 'id_d_nombre', 'id_calle']        
    lista = ['ENVIADO', 'PENDIENTE', 'EN REVISION', 'REVISADO' ,'RECHAZADO']
    
    if observacion:
        fechaObservacion = observacion.fechaCreacion    
        observaciones = ObservacionDocente.objects.filter(observacion = observacion).order_by('-fechaElaboracion')                                
        dias = 5 + observacion.incrementarDias
        fechaObservacion = fechaObservacion + timedelta(days=dias)           
        fechaCorte = fechaObservacion + timedelta(days=1)                     
        fechaObservacion = fechaObservacion.strftime("%d/%b/%Y")                   
    
    if anteproyecto.numIntegrantes == 1: data.append('id_codigoUnion')
                     
    formA = AnteproyectoViewForm(instance = anteproyecto)                                        
    if dependencia:
        formD = DependenciaViewForm(instance = dependencia)
        formT = TitularViewForm(instance = dependencia.titular)
        formDom = DomicilioViewForm(instance = dependencia.domicilio)
    else:
        formD = None
        formT = None
        formDom = None
    formDoc = AnteproyectoDocForm(instance = anteproyecto)
    formAE = AsesorEViewForm(instance = anteproyecto.asesorExterno)     
    formEstado = AnteproyectoEstadoForm(instance = anteproyecto)        
    
    if request.method == 'POST':
        formEstado = AnteproyectoEstadoForm(request.POST, instance = anteproyecto)        
        if formEstado.is_valid():            
            estadoFinal = formEstado['estatus'].value()        
            estudiantes = [i.estudiante for i in all_estudiantes if i.estado == 'ACTIVO' ]                   
            if estadoInicial in lista and estadoFinal == 'ACEPTADO':                
                estudiante_resi = Estudiante_Residencia.objects.filter(estudiante = estudiantes[0], estado='ACTIVO')                
                if not estudiante_resi:     
                    residencia = Residencia(
                        dependencia = dependencia,
                        asesorExterno = anteproyecto.asesorExterno,                    
                        nombre = anteproyecto.a_nombre,
                        tipoProyecto = anteproyecto.tipoProyecto,
                        numIntegrantes = anteproyecto.numIntegrantes                    
                    )        
                    residencia.save()   
                    resi = True                                                                         
                    
                    for e in estudiantes:      
                        estudiante_residencia = Estudiante_Residencia(
                            estudiante = e,
                            residencia = residencia
                            )                      
                        estudiante_residencia.save()                                
            elif estadoFinal == 'CANCELADO':                                
                for e in all_estudiantes:      
                    e.estado = 'INACTIVO'              
                    e.save()
                                       
            formEstado.save()
            asunto = 'El estado de su Anteproyecto se actualizo a: ' + estadoFinal            
            enviar_email(asunto, '', lista_correos, 1, estadoFinal)            
            if resi:
                enviar_email('Su Residencia ha comenzado.', '', lista_correos, 2, 'INICIADA')            
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
    context = {'group': group, 'anteproyecto': anteproyecto, 'estudiantes': estudiantes, 'dependencia': dependencia, 'revisor1': revisor1, 'revisor2': revisor2, 'formA': formA, 'formD': formD, 'formT': formT, 'formAE': formAE ,'formDom': formDom, 'formDoc': formDoc, 'fechaObservacion': fechaObservacion, 'observaciones': observaciones, 'formEstado': formEstado, 'data': data, 'actualizaciones': actualizaciones, 'historial_estudiantes': historial_estudiantes, 'title': 'Anteproyecto'}
    return render(request, 'Admin/verAnteproyecto.html', context)           

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def editarAnteproyectoAdmin(request, pk):
    group = request.user.groups.all()[0].name
    data = ['id_codigoUnion']
    anteproyecto = Anteproyecto.objects.get(id = pk)    
    all_estudiantes = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto)            
    estudiantes = [i.estudiante for i in all_estudiantes ]        
    estudiantes = len(estudiantes)
    #estudiantes = Estudiante.objects.filter(anteproyecto = anteproyecto).count()        
    dependencia = anteproyecto.dependencia
    asesorExterno = anteproyecto.asesorExterno
    titular = dependencia.titular
    domicilio = dependencia.domicilio
    codigo = anteproyecto.codigoUnion
    numIntegrantes = anteproyecto.numIntegrantes
    mensaje = ''    
    
    formA = AnteproyectoEstForm(instance = anteproyecto)                                
    formD = DependenciaForm(instance = dependencia)
    formT = TitularForm(instance = titular)
    formDom = DomicilioForm(instance = domicilio)
    formAE = AsesorEForm(instance = asesorExterno)                 
    
    if request.method == 'POST':                        
        formA = AnteproyectoEstForm(request.POST, instance = anteproyecto)                                
        formD = DependenciaForm(request.POST, instance = dependencia)
        formT = TitularForm(request.POST, instance = titular)
        formDom = DomicilioForm(request.POST, instance = domicilio)
        formAE = AsesorEForm(request.POST, instance = asesorExterno)   
                  
        if formA.is_valid() and formD.is_valid() and formT.is_valid() and formAE.is_valid() and formDom.is_valid():
            numIntegrantes2 = int(formA['numIntegrantes'].value())                                    
            if numIntegrantes2 < 1:
                mensaje = 'El numero de integrantes no puede ser menor a 1'
            else:                
                if numIntegrantes == 1 and numIntegrantes2 >= 2:                    
                    codigo = obtenerCodigo()                    
                elif numIntegrantes >= 2 and numIntegrantes2 == 1 and estudiantes == 1:                    
                    codigo = '0000000000'                                                                                                                                                                                             
                if numIntegrantes > numIntegrantes2 and estudiantes > numIntegrantes2:                                        
                    mensaje = 'No se puede reducir el numero de integrantes. Eliminine algun integrante del anteproyecto para poder reducir el numero de integrantes'                    
                else:                                                
                    domicilio = formDom.save()                  
                    titular = formT.save()              
                    asesorExterno = formAE.save()      
                    dependencia = formD.save()            
                    anteproyecto = formA.save()
                    anteproyecto.dependencia = dependencia
                    anteproyecto.asesorExterno = asesorExterno
                    anteproyecto.codigoUnion = codigo
                    asesorExterno.dependencia = dependencia
                    asesorExterno.save()                                    
                    anteproyecto.save() 
                    return redirect('verAnteproyecto', pk = anteproyecto.id)                               
    
    context = {'group': group, 'formA': formA, 'formD': formD, 'formT': formT, 'formAE': formAE ,'formDom': formDom, 'anteproyecto': anteproyecto, 'dependencia': dependencia, 'mensaje': mensaje, 'group': group, 'data': data, 'title': 'Editar Anteproyecto'}                
    return render(request, 'Admin/editarAnteproyecto.html', context)        

@admin_only
def eliminarAnteproyecto(request, pk):    
    anteproyecto = Anteproyecto.objects.get(id = pk)
    all_estudiante_anteproyecto = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto)
    for i in all_estudiante_anteproyecto:
        i.delete()
    anteproyecto.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarResidencia(request, pk):    
    residencia = Residencia.objects.get(id = pk)
    all_estudiante_residencia = Estudiante_Residencia.objects.filter(residencia = residencia)
    for i in all_estudiante_residencia:
        i.delete()
    residencia.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def editarObservaciones(request, pk):
    group = request.user.groups.all()[0].name
    docente = None
    anteproyecto = Anteproyecto.objects.get(id = pk)
    observacion = anteproyecto.observacion
    fechaObservacion = None
    observaciones = None
    dias = 0
    fechaCorte = None
    fechaActual = date.today    
    
    estudiantes = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto, estado = 'ACTIVO')    
    lista_correos = [i.estudiante.correoElectronico for i in estudiantes]
    
    if observacion:
        fechaObservacion = observacion.fechaCreacion    
        observaciones = ObservacionDocente.objects.filter(observacion = observacion).order_by('-fechaElaboracion')                                
        dias = 5 + observacion.incrementarDias
        fechaObservacion = fechaObservacion + timedelta(days=dias)           
        fechaCorte = fechaObservacion + timedelta(days=1)                     
        fechaObservacion = fechaObservacion.strftime("%d/%b/%Y")                   
        
    if request.method == 'POST':                
        
        try:
            rDias = int(request.POST['agregarDias'])
        except: 
            rDias = None
            
        try:
            rObservacion = request.POST['Dobservacion']
        except: 
            rObservacion = None
        
        if observacion:    
            if rDias and rDias > 0:                  
                observacion.incrementarDias += rDias            
                observacion.save()
                
            if rObservacion:            
                nuevaObservacion = ObservacionDocente(
                    docente = docente,
                    observacion = observacion,
                    observacionD = rObservacion
                )
                nuevaObservacion.save()                   
                asunto = 'Tiene una nueva observacion'            
                enviar_email(asunto, '', lista_correos, 3)                 
        else:                            
                
            if rObservacion:            
                observacion = Observacion()
                observacion.save()
                anteproyecto.observacion = observacion
                anteproyecto.save()        
                nuevaObservacion = ObservacionDocente(
                    docente = docente,
                    observacion = observacion,
                    observacionD = rObservacion
                )
                nuevaObservacion.save()  
                
                asunto = 'Tiene una nueva observacion'            
                enviar_email(asunto, '', lista_correos, 3)          
                                    
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))                    
    
    context = {'anteproyecto': anteproyecto, 'group': group, 'observaciones': observaciones, 'fechaObservacion': fechaObservacion, 'fechaCorte': fechaCorte, 'fechaActual': fechaActual, 'title': 'Editar Observaciones'}    
    return render(request, 'Admin/editObservaciones.html', context)        

@admin_only
def eliminarObservacion(request, pk):    
    observacion = ObservacionDocente.objects.get(id = pk)    
    observacion.delete()    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@publicView
def verEstudiante(request, pk):
    group = request.user.groups.all()[0].name
    estudiante = Estudiante.objects.get(id = pk)
    domicilio = estudiante.domicilio    
    
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')    
    all_residencias = Estudiante_Residencia.objects.filter(estudiante = estudiante, estado = 'ACTIVO')        
    
    all_anteproyectos_c = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'INACTIVO').count()    
    all_residencias_c = Estudiante_Residencia.objects.filter(estudiante = estudiante, estado = 'INACTIVO').count()        
    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto    
    else:
        anteproyecto = None      
    
    if all_residencias:        
        residencia = all_residencias[0].residencia    
    else:
        residencia = None      
                
    expediente = estudiante.expediente
    
    context = {'group': group, 'estudiante': estudiante, 'domicilio': domicilio, 'anteproyecto': anteproyecto, 'residencia': residencia, 'expediente': expediente, 'all_anteproyectos_c': all_anteproyectos_c, 'all_residencias_c': all_residencias_c, 'title': 'Estudiante'}    
    return render(request, 'Admin/verEstudiante.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def editarEstudiante(request, pk):
    group = request.user.groups.all()[0].name
    estudiante = Estudiante.objects.get(id = pk)
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto    
    else:
        anteproyecto = None      
    
    domicilio = estudiante.domicilio
    
    formE = EstudianteForm(instance=estudiante)
    formD = DomicilioForm(instance=domicilio)
    
    if request.method == 'POST':
        formE = EstudianteForm(request.POST, instance=estudiante)
        formD = DomicilioForm(request.POST, instance=domicilio)
    
        if formE.is_valid():
            formE.save()
            
        if not domicilio:    
            if formD.is_valid():
                formD.save()
    
        return redirect('verEstudiante', estudiante.id)
    
    context = {'group': group, 'estudiante': estudiante, 'anteproyecto': anteproyecto, 'formE': formE, 'formD': formD, 'title': 'Editar Estudiante'}    
    return render(request, 'Student/settings.html', context)        

@admin_only
def removeEstudiante(request, pk):    
    estudiante = Estudiante.objects.get(id = pk)
    estudiante_anteproyecto = Estudiante_Anteproyecto.objects.get(estudiante = estudiante)
    estudiante_anteproyecto.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def asignarRevisor1(request, page, pk):
    group = request.user.groups.all()[0].name
    anteproyecto = Anteproyecto.objects.get(id = pk)        
    all_docentes = Docente.objects.filter(estatus = 'ACTIVO')        
    start = (page-1)*10    
    end = page*10
    
    anteproyecto_v = Anteproyecto.objects.filter(id = pk).values()
    anteproyecto_list = list(anteproyecto_v)    
    anteproyecto_materia_list = list(Anteproyecto_materia.objects.filter(anteproyecto = anteproyecto).values())
    materia_list = list(Materia.objects.all().values())
    docente_list = list(all_docentes.values())
    perfil_academico_list = list(PerfilAcademico.materias.through.objects.all().values())
    df_anteproyectos = pd.DataFrame(anteproyecto_list)
    df_anteproyecto_materia = pd.DataFrame(anteproyecto_materia_list)
    df_docentes = pd.DataFrame(docente_list)
    df_perfil_academico = pd.DataFrame(perfil_academico_list)
    df_materias = pd.DataFrame(materia_list)    
    docentes_id_list = recomendaciones_docentes(df_anteproyectos, df_anteproyecto_materia, df_docentes, df_perfil_academico, df_materias)                
    #recomendaciones = all_docentes.filter(id__in = docentes_id_list)
    recomendaciones = []
    for i in docentes_id_list:
        try:
            d = all_docentes.get(id = i)
            recomendaciones.append(d)
        except:
            pass    

    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_docentes = buscar_docente(all_docentes, text, opc)                        
            docentes = all_docentes
            start = 0
            end = docentes.count()
            totalD = all_docentes.count()            
            revisor1 = '.'                 
            context = {'group': group, 'anteproyecto': anteproyecto, 'revisor1': revisor1, 'docentes': docentes, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'title': 'Asignar Revisor'}    
            return render(request, 'Admin/asignarDocente.html', context)                    
    
    docentes = all_docentes[start:end]    
    if end != docentes.count():
        end = end-10+docentes.count()
    totalD = all_docentes.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1            
    revisor1 = '.'
    
    context = {'group': group, 'docentes': docentes, 'anteproyecto': anteproyecto, 'revisor1': revisor1, 'totalD': totalD, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'recomendaciones': recomendaciones, 'title': 'Asignar Revisor'}
    return render(request, 'Admin/asignarDocente.html', context)        

@admin_only
def asignarRevisor1I(request, pkA, pkD):        
    anteproyecto = Anteproyecto.objects.get(id = pkA)
    docente = Docente.objects.get(id = pkD)
    anteproyecto.revisor1 = docente
    revisor2 = anteproyecto.revisor2
    all_estudiantes = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto, estado = 'ACTIVO')                
    estudiantes = [i.estudiante for i in all_estudiantes ]         
    lista_correos = [i.estudiante.correoElectronico for i in all_estudiantes]            
    estudiantes_str = "\n".join(str(x) for x in estudiantes)
    
    if revisor2 and anteproyecto.estatus != 'ACEPTADO':
        anteproyecto.estatus = 'EN REVISION'
        asunto = 'El estado de su Anteproyecto se actualizo a: EN REVISION'
        mensaje = ('Feliciades, ya le han sido asignados ambos revisores a su anteproyecto. Le recomendamos ponerse en contacto con ellos lo mas pronto posible.'  + '\n'
                   + '*' + '\n'
                   + 'Revisor 1: ' + str(docente) + '\n'
                   + 'Correo Electronico: ' + docente.correoElectronico + '\n'
                   + '*' + '\n'
                   + 'Revisor 2: ' + str(revisor2) + '\n'
                   + 'Correo Electronico: ' + revisor2.correoElectronico + '\n' + '\n'
                   + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.') 
        enviar_email(asunto, mensaje, lista_correos,)            
    anteproyecto.save()   
     
    mensaje = ('Buenos días,' + "\n" + 'Se informa que ha sido asignado como revisor 1 del anteproyecto de residencia profesional.' + "\n"
               + 'Nombre del anteproyecto: ' + anteproyecto.a_nombre + "\n"               
               + 'Integrante(s):' + "\n" + estudiantes_str + "\n"
               + 'Correo electronico:' + "\n" + "\n".join(lista_correos) + '\n' + '\n'
               + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
    enviar_email('Asignacion revisor anteproyecto', mensaje, [docente.correoElectronico])
        
    return redirect('verAnteproyecto', anteproyecto.id)

@admin_only
def removeRevisor1(request, pk):
    anteproyecto = Anteproyecto.objects.get(id = pk)
    anteproyecto.revisor1 = None
    anteproyecto.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def asignarRevisor2(request, page, pk):
    group = request.user.groups.all()[0].name
    anteproyecto = Anteproyecto.objects.get(id = pk)
    all_docentes = Docente.objects.filter(estatus = 'ACTIVO')        
    start = (page-1)*10    
    end = page*10
    
    anteproyecto_v = Anteproyecto.objects.filter(id = pk).values()
    anteproyecto_list = list(anteproyecto_v)    
    anteproyecto_materia_list = list(Anteproyecto_materia.objects.filter(anteproyecto = anteproyecto).values())
    materia_list = list(Materia.objects.all().values())
    docente_list = list(all_docentes.values())
    perfil_academico_list = list(PerfilAcademico.materias.through.objects.all().values())
    df_anteproyectos = pd.DataFrame(anteproyecto_list)
    df_anteproyecto_materia = pd.DataFrame(anteproyecto_materia_list)
    df_docentes = pd.DataFrame(docente_list)
    df_perfil_academico = pd.DataFrame(perfil_academico_list)
    df_materias = pd.DataFrame(materia_list)
    docentes_id_list = recomendaciones_docentes(df_anteproyectos, df_anteproyecto_materia, df_docentes, df_perfil_academico, df_materias)            
    #recomendaciones = all_docentes.filter(id__in = docentes_id_list)    
    recomendaciones = []
    for i in docentes_id_list:
        try:
            d = all_docentes.get(id = i)
            recomendaciones.append(d)
        except:
            pass    
    
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_docentes = buscar_docente(all_docentes, text, opc)                                    
            docentes = all_docentes
            start = 0
            end = docentes.count()
            totalD = all_docentes.count()            
            revisor2 = '.'                 
            context = {'group': group, 'anteproyecto': anteproyecto, 'revisor2': revisor2, 'docentes': docentes, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'title': 'Asignar Revisor'}    
            return render(request, 'Admin/asignarDocente.html', context)                    
    
    docentes = all_docentes[start:end]    
    if end != docentes.count():
        end = end-10+docentes.count()
    totalD = all_docentes.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1            
    
    revisor2 = '.'
    context = {'group': group, 'docentes': docentes, 'anteproyecto': anteproyecto, 'revisor2': revisor2, 'totalD': totalD, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'recomendaciones': recomendaciones, 'title': 'Asignar Revisor'}
    return render(request, 'Admin/asignarDocente.html', context)        

@admin_only
def asignarRevisor2I(request, pkA, pkD):        
    anteproyecto = Anteproyecto.objects.get(id = pkA)
    docente = Docente.objects.get(id = pkD)
    anteproyecto.revisor2 = docente
    revisor1 = anteproyecto.revisor1
    all_estudiantes = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto, estado = 'ACTIVO')            
    estudiantes = [i.estudiante for i in all_estudiantes ]                
    lista_correos = [i.estudiante.correoElectronico for i in all_estudiantes ]            
    estudiantes_str = "\n".join(str(x) for x in estudiantes)
    
    if revisor1 and anteproyecto.estatus != 'ACEPTADO':
        anteproyecto.estatus = 'EN REVISION'
        asunto = 'El estado de su Anteproyecto se actualizo a: EN REVISION'
        mensaje = ('Feliciades, ya le han sido asignados ambos revisores a su anteproyecto. Le recomendamos ponerse en contacto con ellos lo mas pronto posible.'  + '\n'
                   + '*' + '\n'
                   + 'Revisor 1: ' + str(revisor1) + '\n'
                   + 'Correo Electronico: ' + revisor1.correoElectronico + '\n'
                   + '*' + '\n'
                   + 'Revisor 2: ' + str(docente) + '\n'
                   + 'Correo Electronico: ' + docente.correoElectronico + '\n' + '\n'
                   + 'Atentamente,' + "\n" + 'El equipo del Depto. de vinculación de sistemas y computación.')
        enviar_email(asunto, mensaje, lista_correos)          
    anteproyecto.save()     
    mensaje = ('Buenos días,' + "\n" + 'Se informa que ha sido asignado como revisor 2 del anteproyecto de residencia profesional.' + "\n"
               + 'Nombre del anteproyecto: ' + anteproyecto.a_nombre + "\n"               
               + 'Integrante(s):' + "\n" + estudiantes_str + "\n"
               + 'Correo electronico:' + "\n" + "\n".join(lista_correos) + '\n' + '\n'
               + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
    enviar_email('Asignacion revisor anteproyecto', mensaje, [docente.correoElectronico])   
    return redirect('verAnteproyecto', anteproyecto.id)

@admin_only
def removeRevisor2(request, pk):
    anteproyecto = Anteproyecto.objects.get(id = pk)
    anteproyecto.revisor2 = None
    anteproyecto.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@publicView
def verDocente(request, pk):
    group = request.user.groups.all()[0].name
    docente = Docente.objects.get(id = pk)   
    all_anteproyectos = Anteproyecto.objects.all()
    all_residencias = Residencia.objects.all()
    
    try:
        perfilAcademico = docente.perfilAcademico
        materias = perfilAcademico.materias.all()                
    except:
        perfilAcademico = None
        materias = None
    
    anteproyectos_activos_r1 = all_anteproyectos.filter(revisor1=docente).exclude(estatus__in=['ACEPTADO', 'RECHAZADO'])
    anteproyectos_activos_r2 = all_anteproyectos.filter(revisor2=docente).exclude(estatus__in=['ACEPTADO', 'RECHAZADO'])
    
    residencias_activas_a = all_residencias.filter(r_asesorInterno=docente).exclude(estatus__in=['FINALIZADA', 'RECHAZADA', 'NO FINALIZADA'])
    residencias_activas_r = all_residencias.filter(r_revisor=docente).exclude(estatus__in=['FINALIZADA', 'RECHAZADA', 'NO FINALIZADA'])
    
    anteproyectos_pasados_r1 = all_anteproyectos.filter(estatus='ACEPTADO', revisor1=docente)
    anteproyectos_pasados_r2 = all_anteproyectos.filter(estatus='ACEPTADO', revisor2=docente)
    
    residencias_pasadas_a = all_residencias.filter(estatus='FINALIZADA', r_asesorInterno=docente)
    residencias_pasadas_r = all_residencias.filter(estatus='FINALIZADA', r_revisor=docente)            
         
    actividad_docente = [anteproyectos_activos_r1.count() + anteproyectos_activos_r2.count(),
                         residencias_activas_a.count() + residencias_activas_r.count(), 
                         residencias_activas_a.count(), 
                         anteproyectos_pasados_r1.count() + anteproyectos_pasados_r2.count(), 
                         residencias_pasadas_a.count() + residencias_pasadas_r.count(), 
                         residencias_activas_r.count()
                         ]
            
    context = {'group': group, 'docente': docente, 'actividad_docente': actividad_docente, 'materias': materias, 'title': 'Ver Docente'}        
    return render(request, 'Admin/verDocente.html', context)    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def editarDocente(request, pk):
    group = request.user.groups.all()[0].name
    docente = Docente.objects.get(id = pk)
    formD = DocenteForm(instance=docente)
    
    try:
        perfilAcademico = docente.perfilAcademico
        materias = perfilAcademico.materias.all()        
    except:
        perfilAcademico = None
        materias = None
        
    if request.method == 'POST':
        formD = DocenteForm(request.POST, request.FILES, instance=docente)
        if formD.is_valid():
            formD.save()
            return redirect('verDocente', docente.id)
            
    
    context = {'group': group, 'docente': docente, 'formD': formD, 'materias': materias, 'title': 'Editar Docente'}
    return render(request, 'Admin/editarDocente.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def altaDocente(request):
    group = request.user.groups.all()[0].name
    data = ['id_fotoUsuario', 'id_correoElectronico']
    formD = DocenteForm()
    formU = CreateUserFormDocente()
    
    if request.method == 'POST':
        formD = DocenteForm(request.POST)
        formU = CreateUserFormDocente(request.POST)
        
        if formD.is_valid() and formU.is_valid():
            teacher = formD.save()
            user = formU.save()
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            teacher.correoElectronico = formU.cleaned_data.get('email')            
            teacher.user = user
            teacher.save()
            
            return redirect('docentes', 1, 0)
    
    context = {'group': group, 'formD': formD, 'formU': formU, 'data': data, 'title': 'Alta Docente'}
    return render(request, 'Admin/altaDocente.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@publicView
def verResidencia(request, pk):
    group = request.user.groups.all()[0].name
    data = ['id_mision', 'id_tipoProyecto', 'id_calle', 'id_d_nombre', 'id_nombre']        
    residencia = Residencia.objects.get(id = pk)    
    all_estudiantes = Estudiante_Residencia.objects.filter(residencia = residencia)            
    estudiantes = [i.estudiante for i in all_estudiantes ]     
    all_estudiantes_a = all_estudiantes.filter(estado = 'ACTIVO')              
    lista_correos = [i.estudiante.correoElectronico for i in all_estudiantes_a ]
    
    for i in estudiantes:        
        residencia_e = all_estudiantes.filter(estudiante = i)        
        
        if residencia_e:
            estado_residencia = residencia_e[0].estado
        else:
            estado_residencia = None                    
                    
        setattr(i, 'residencia_estatus', estado_residencia)          
    
    asesorI = residencia.r_asesorInterno
    revisor = residencia.r_revisor
    dependencia = residencia.dependencia
    formR = ResidenciaViewForm(instance = residencia)                                
    formD = DependenciaViewForm(instance = dependencia)
    formDom = DomicilioViewForm(instance = dependencia.domicilio)
    formER = ResidenciaEstadoForm(instance = residencia)
    
    if request.method == 'POST':
        formER = ResidenciaEstadoForm(request.POST, instance = residencia)        
        if formER.is_valid():  
            estadoFinal = formER['estatus'].value()  
            if estadoFinal == 'CANCELADA':                
                anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiantes[0], estado = 'ACTIVO')  
                
                if anteproyecto:
                    anteproyecto = anteproyecto[0].anteproyecto
                    all_estudiantes_ant = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto, estado = 'ACTIVO')                      
                    anteproyecto.estatus = 'CANCELADO'
                    anteproyecto.save()
                    for i in all_estudiantes_ant:
                        i.estado = 'INACTIVO'
                        i.save()                    
                
                for i in all_estudiantes:
                    i.estado = 'INACTIVO'
                    i.save()
            asunto = 'El estado de su Residencia se actualizo a: ' + estadoFinal
            
            enviar_email(asunto, '', lista_correos, 2, estadoFinal)
            formER.save()      
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))    
            
    context = {'group': group, 'residencia': residencia, 'estudiantes': estudiantes, 'asesorI': asesorI, 'revisor': revisor, 'dependencia': dependencia, 'formR': formR, 'formD': formD, 'formER': formER, 'formDom': formDom, 'data': data, 'title': 'Ver Residencia'}
    return render(request, 'Admin/verResidencia.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def editarResidenciaAdmin(request, pk):
    group = request.user.groups.all()[0].name
    residencia = Residencia.objects.get(id = pk)    
    all_estudiantes = Estudiante_Residencia.objects.filter(residencia = residencia)            
    estudiantes = [i.estudiante for i in all_estudiantes ]        
    estudiantes = len(estudiantes)
    #estudiantes = Estudiante.objects.filter(residencia = residencia).count()        
    dependencia = residencia.dependencia
    asesorExterno = residencia.asesorExterno
    titular = dependencia.titular
    domicilio = dependencia.domicilio    
    numIntegrantes = residencia.numIntegrantes
    mensaje = ''    
    
    formR = ResidenciaForm(instance = residencia)                                
    formD = DependenciaForm(instance = dependencia)
    formT = TitularForm(instance = titular)
    formDom = DomicilioForm(instance = domicilio)
    formAE = AsesorEForm(instance = asesorExterno)    
    
    if request.method == 'POST':                        
        formR = ResidenciaForm(request.POST, instance = residencia)                                
        formD = DependenciaForm(request.POST, instance = dependencia)
        formT = TitularForm(request.POST, instance = titular)
        formDom = DomicilioForm(request.POST, instance = domicilio)
        formAE = AsesorEForm(request.POST, instance = asesorExterno)   
                  
        if formR.is_valid() and formD.is_valid() and formT.is_valid() and formAE.is_valid() and formDom.is_valid():
            numIntegrantes2 = int(formR['numIntegrantes'].value())                                    
            if numIntegrantes2 < 1:
                mensaje = 'El numero de integrantes no puede ser menor a 1'
            else:                                                                                                                                                                                  
                if numIntegrantes > numIntegrantes2 and estudiantes > numIntegrantes2:                                        
                    mensaje = 'No se puede reducir el numero de integrantes. Eliminine algun integrante del anteproyecto para poder reducir el numero de integrantes'                    
                else:                                                
                    domicilio = formDom.save()                  
                    titular = formT.save()              
                    asesorExterno = formAE.save()      
                    dependencia = formD.save()            
                    residencia = formR.save()
                    residencia.dependencia = dependencia
                    residencia.asesorExterno = asesorExterno                    
                    asesorExterno.dependencia = dependencia
                    asesorExterno.save()                                    
                    residencia.save() 
                    return redirect('verResidencia', pk = residencia.id)                                 
    
    context = {'group': group, 'formR': formR, 'formD': formD, 'formT': formT, 'formDom': formDom, 'formAE': formAE, 'residencia': residencia, 'mensaje':mensaje, 'title': 'Editar Residencia'}    
    return render(request, 'Admin/editarResidencia.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def asignarAsesorIL(request, page, pk):
    group = request.user.groups.all()[0].name
    residencia = Residencia.objects.get(id = pk)        
    all_docentes = Docente.objects.filter(estatus = 'ACTIVO')
    start = (page-1)*10    
    end = page*10
    estudiante = Estudiante_Residencia.objects.filter(residencia = residencia, estado = 'ACTIVO')[0].estudiante    
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto
    revisores = [anteproyecto.revisor1, anteproyecto.revisor2]
        
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_docentes = buscar_docente(all_docentes, text, opc)                                    
            docentes = all_docentes
            start = 0
            end = docentes.count()
            totalD = all_docentes.count()            
            asesorI = '.'                 
            context = {'group': group, 'residencia': residencia, 'asesorI': asesorI, 'docentes': docentes, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'title': 'Asignar Asesor I'}    
            return render(request, 'Admin/asignarDocente.html', context)                    
        
    docentes = all_docentes[start:end]    
    if end != docentes.count():
        end = end-10+docentes.count()
    totalD = all_docentes.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1        
    asesorI = '.'
    context = {'group': group, 'residencia': residencia, 'asesorI':asesorI, 'docentes': docentes, 'totalD': totalD, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'revisores': revisores, 'title': 'Asignar Asesor I'}
    return render(request, 'Admin/asignarDocente.html', context)            

@admin_only
def asignarAsesorI(request, pkR, pkD):
    residencia = Residencia.objects.get(id = pkR)
    docente = Docente.objects.get(id = pkD)
    residencia.r_asesorInterno = docente   
    revisor = residencia.r_revisor 
    all_estudiantes = Estudiante_Residencia.objects.filter(residencia = residencia, estado = 'ACTIVO')            
    estudiantes = [i.estudiante for i in all_estudiantes ]                
    lista_correos = [i.estudiante.correoElectronico for i in all_estudiantes ]            
    estudiantes_str = "\n".join(str(x) for x in estudiantes)
    
    if revisor and residencia.estatus == 'INICIADA':        
        residencia.estatus = 'EN PROCESO'
        asunto = 'El estado de su Residencia se actualizo a: EN PROCESO'
        mensaje = ('¡Felicidades!, ya le han sido asignado un asesor interno y un revisor a su proyecto de residencia. Le recomendamos ponerse en contacto con ellos lo más pronto posible.'  + '\n'
                   + '*' + '\n'
                   + 'Asesor Interno: ' + str(docente) + '\n'
                   + 'Correo Electronico: ' + docente.correoElectronico + '\n'
                   + '*' + '\n'
                   + 'Revisor: ' + str(revisor) + '\n'
                   + 'Correo Electronico: ' + revisor.correoElectronico + '\n' + '\n'
                   + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
        enviar_email(asunto, mensaje, lista_correos,)    
    
    mensaje = ('Buenos días,' + "\n" + 'Se le informa que usted ha sido asignado como Asesor Interno del siguiente proyecto de residencia.' + "\n"
               + 'Nombre del proyecto: ' + residencia.nombre + "\n"               
               + 'Integrante(s):' + "\n" + estudiantes_str + "\n"
               + 'Correo electronico:' + "\n" + "\n".join(lista_correos) + '\n' + '\n'
               + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
    enviar_email('Asignacion asesor interno proyecto de residencia', mensaje, [docente.correoElectronico])            
    residencia.save()
    return redirect('verResidencia', residencia.id)

@admin_only
def removeAsesorI(request, pk):
    residencia = Residencia.objects.get(id = pk)
    residencia.r_asesorInterno = None
    residencia.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def asignarRevisorL(request, page, pk):
    group = request.user.groups.all()[0].name
    residencia = Residencia.objects.get(id = pk)    
    all_docentes = Docente.objects.all()        
    start = (page-1)*10    
    end = page*10           
    estudiante = Estudiante_Residencia.objects.filter(residencia = residencia, estado = 'ACTIVO')[0].estudiante    
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto
    #estudiante = Estudiante.objects.filter(residencia = residencia)[0]
    #anteproyecto = estudiante.anteproyecto
    revisores = [anteproyecto.revisor1, anteproyecto.revisor2]                 
    
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_docentes = buscar_docente(all_docentes, text, opc)                                    
            docentes = all_docentes
            start = 0
            end = docentes.count()
            totalD = all_docentes.count()            
            revisor = '.'                 
            context = {'group': group, 'residencia': residencia, 'revisor': revisor, 'docentes': docentes, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'title': 'Asignar Revisor'}    
            return render(request, 'Admin/asignarDocente.html', context)                    
    
    docentes = all_docentes[start:end]        
    if end != docentes.count():
        end = end-10+docentes.count()
    totalD = all_docentes.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1        
    revisor = '.'        
    
    context = {'group': group, 'residencia': residencia, 'revisor': revisor, 'docentes': docentes, 'totalD': totalD, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'revisores':revisores, 'title': 'Asignar Revisor'}    
    return render(request, 'Admin/asignarDocente.html', context)            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def avisos(request):
    group = request.user.groups.all()[0].name
    avisos = Avisos.objects.all().order_by('-fechaCreacion')        
    context = {'group': group, 'avisos': avisos, 'title': 'Avisos'}
    return render(request, 'Admin/avisos.html', context)            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def crear_aviso(request):
    group = request.user.groups.all()[0].name
    form = AvisosForm()
    if request.method == 'POST':
        form = AvisosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('avisos')
    context = {'group': group, 'form': form, 'title': 'Crear Aviso'}
    return render(request, 'Admin/crearAviso.html', context)            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def materias_a(request, page, orderB, filter):
    group = request.user.groups.all()[0].name    
    all_materias = Materia.objects.all()
    start = (page-1)*10    
    end = page*10                    
        
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_materias = buscar_materia(all_materias, text, opc)                                                                                            
            materias = all_materias
            start = 0
            end = materias.count()
            totalD = all_materias.count()                        
            search = '.'      
            context = {'group': group, 'materias': materias, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'title': 'Materias'}
            return render(request, 'Admin/materias.html', context)            
    
    all_materias = filtrar_materias(all_materias, filter)            
    all_materias = ordenar_materias(all_materias, orderB)
    materias = all_materias[start:end]    
    if end != materias.count():
        end = end-10+materias.count()
    totalD = all_materias.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    context = {'group': group, 'materias': materias, 'totalD': totalD, 'buttons': buttons, 'page': page, 'filter': filter, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'orderB': orderB, 'title': 'Materias'}
    return render(request, 'Admin/materias.html', context)     

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def editarMateria(request, pk):
    group = request.user.groups.all()[0].name    
    materia = Materia.objects.get(id = pk)
    form =  MateriaForm(instance = materia)
    
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance = materia)
        if form.is_valid():
            form.save()
            return redirect('materias_a', 1, 0, 0)
    
    context = {'group': group, 'materia': materia, 'form': form, 'title': 'Editar Materia'}
    return render(request, 'Admin/editar_materia.html', context)            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def altaMateria(request):
    group = request.user.groups.all()[0].name    
    form = MateriaForm()    
    
    if request.method == 'POST':
        form = MateriaForm(request.POST)            
        if form.is_valid():            
            form.save()                            
            return redirect('materias_a', 1, 0, 0)
    
    context = {'group': group, 'form': form, 'title': 'Alta Materia'}
    return render(request, 'Admin/alta_materia.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def dependencias_a(request, page, orderB, filter):
    group = request.user.groups.all()[0].name    
    all_dependencias = Dependencia.objects.all()
    start = (page-1)*10    
    end = page*10                    
        
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'] 
                        
        if text:
            all_dependencias = buscar_dependencia(all_dependencias, text, opc)                                                                                            
            dependencias = all_dependencias
            start = 0
            end = dependencias.count()
            totalD = all_dependencias.count()                        
            search = '.'      
            context = {'group': group, 'dependencias': dependencias, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'title': 'Organizaciones o Empresas'}
            return render(request, 'Admin/dependencias.html', context)            
    
    all_dependencias = filtrar_dependencias(all_dependencias, filter)            
    all_dependencias = ordenar_dependencias(all_dependencias, orderB)
    dependencias = all_dependencias[start:end]    
    if end != dependencias.count():
        end = end-10+dependencias.count()
    totalD = all_dependencias.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    context = {'group': group, 'dependencias': dependencias, 'totalD': totalD, 'buttons': buttons, 'page': page, 'filter': filter, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'orderB': orderB, 'title': 'Organizaciones o Empresas'}
    return render(request, 'Admin/dependencias.html', context)     

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def ver_dependencia(request, pk):
    group = request.user.groups.all()[0].name   
    data = ['id_mision', 'id_d_nombre', 'id_calle'] 
    dependencia = Dependencia.objects.get(id = pk)
    domicilio = dependencia.domicilio
    titular = dependencia.titular
    
    formD =  DependenciaViewForm(instance = dependencia)
    formDom = DomicilioViewForm(instance = domicilio)
    formT = TitularViewForm(instance = titular)
    
    context = {'group': group, 'dependencia': dependencia, 'formD': formD, 'formDom': formDom, 'formT': formT, 'data': data, 'title': 'Ver Dependencia'}
    return render(request, 'Admin/ver_dependencia.html', context)  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def editar_dependencia(request, pk):
    group = request.user.groups.all()[0].name   
    data = ['id_mision', 'id_d_nombre', 'id_calle'] 
    dependencia = Dependencia.objects.get(id = pk)
    domicilio = dependencia.domicilio    
    titular = dependencia.titular
    formD =  DependenciaForm(instance = dependencia)
    formDom = DomicilioForm(instance = domicilio)
    formT = TitularForm(instance = titular)
    
    if request.method == 'POST':
        formD = DependenciaForm(request.POST, instance = dependencia)
        formDom = DomicilioForm(request.POST, instance = domicilio)
        formT = TitularForm(request.POST, instance = titular)
        if formD.is_valid() and formDom.is_valid() and formT.is_valid():
            formD.save()
            formDom.save()
            formT.save()
            return redirect('dependencias_a', 1, 0, 0)
    
    context = {'group': group, 'data': data, 'dependencia': dependencia, 'formD': formD, 'formDom': formDom, 'formT': formT, 'title': 'Editar Dependencia'}
    return render(request, 'Admin/editar_dependencia.html', context)            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def altaDependencia(request):
    group = request.user.groups.all()[0].name    
    form = DependenciaForm()
    
    if request.method == 'POST':
        form = DependenciaForm(request.POST)            
        if form.is_valid():            
            dependencia = form.save()                                        
            return redirect('alta_titular_dep', dependencia.id)
    
    context = {'group': group, 'form': form, 'title': 'Alta Organización o Empresa'}
    return render(request, 'Admin/alta_dependencia.html', context)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def alta_titular_dep(request, pk):
    group = request.user.groups.all()[0].name    
    dependencia = Dependencia.objects.get(id = pk)
    form = TitularForm()
        
    if request.method == 'POST':
        form = TitularForm(request.POST)            
        if form.is_valid():
            titular = form.save()
            titular.save()
            dependencia.titular = titular
            dependencia.save()
            if not dependencia.domicilio:
                return redirect('alta_domicilio_dep', dependencia.id)                                                            
            else:
                return redirect('ver_dependencia', dependencia.id)   
    
    context = {'group': group, 'dependencia': dependencia, 'form': form, 'title': 'Alta Titular de la Organización o Empresa'}
    return render(request, 'Admin/alta_titular.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def alta_domicilio_dep(request, pk):
    group = request.user.groups.all()[0].name    
    dependencia = Dependencia.objects.get(id = pk)
    form = DomicilioForm()
        
    if request.method == 'POST':
        form = DomicilioForm(request.POST)            
        if form.is_valid():
            domicilio = form.save()
            domicilio.save()
            dependencia.domicilio = domicilio
            dependencia.save()
            if not dependencia.titular:
                return redirect('alta_titular_dep', dependencia.id)                                                            
            else:
                return redirect('ver_dependencia', dependencia.id)   
    
    context = {'group': group, 'dependencia': dependencia, 'form': form, 'title': 'Alta Domicilio de la Organización o Empresa'}
    return render(request, 'Admin/alta_domicilio_dep.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def historial_estudiante(request, pk):
    group = request.user.groups.all()[0].name    
    estudiante = Estudiante.objects.get(id = pk)                
    
    anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante)        
    residencias = Estudiante_Residencia.objects.filter(estudiante = estudiante)        
    
    context = {'group': group, 'estudiante': estudiante, 'anteproyectos': anteproyectos, 'residencias': residencias, 'title': 'Historial Estudiante'}
    return render(request, 'Admin/historial_estudiante.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def asignarRevisor(request, pkR, pkD):
    residencia = Residencia.objects.get(id = pkR)
    docente = Docente.objects.get(id = pkD)
    residencia.r_revisor = docente
    asesor_interno = residencia.r_asesorInterno
    all_estudiantes = Estudiante_Residencia.objects.filter(residencia = residencia, estado = 'ACTIVO')            
    estudiantes = [i.estudiante for i in all_estudiantes ]                
    lista_correos = [i.estudiante.correoElectronico for i in all_estudiantes ]            
    estudiantes_str = "\n".join(str(x) for x in estudiantes)    
       
    if asesor_interno and residencia.estatus == 'INICIADA':        
        residencia.estatus = 'EN PROCESO'
        asunto = 'El estado de su Residencia se actualizo a: EN PROCESO'
        mensaje = ('¡Felicidades!, ya le han sido asignado un asesor interno y un revisor a su proyecto de residencia. Le recomendamos ponerse en contacto con ellos lo más pronto posible.'  + '\n'
                   + '*' + '\n'
                   + 'Asesor Interno: ' + str(asesor_interno) + '\n'
                   + 'Correo Electronico: ' + asesor_interno.correoElectronico + '\n'
                   + '*' + '\n'
                   + 'Revisor: ' + str(docente) + '\n'
                   + 'Correo Electronico: ' + docente.correoElectronico + '\n' + '\n'
                   + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
        enviar_email(asunto, mensaje, lista_correos,)        
    residencia.save()
    mensaje = ('Buenos días,' + "\n" + 'Se le informa que usted ha sido asignado como Revisor del siguiente proyecto de residencia.' + "\n"
               + 'Nombre del proyecto: ' + residencia.nombre + "\n"               
               + 'Integrante(s):' + "\n" + estudiantes_str + "\n"
               + 'Correo electronico:' + "\n" + "\n".join(lista_correos)  + '\n' + '\n'
               + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
    enviar_email('Asignacion revisor proyecto de residencia', mensaje, [docente.correoElectronico])            
    return redirect('verResidencia', residencia.id)

@admin_only
def removeRevisor(request, pk):
    residencia = Residencia.objects.get(id = pk)
    residencia.r_revisor = None
    residencia.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarEstudiante(request, pk):
    estudiante = Estudiante.objects.get(id = pk)
    usuario = estudiante.user
    usuario.delete()
    estudiante.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarDocente(request, pk):
    docente = Docente.objects.get(id = pk)
    usuario = docente.user
    usuario.delete()
    docente.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarMateria(request, pk):
    materia = Materia.objects.get(id = pk)
    materia.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminar_dependencia(request, pk):
    dependencia = Dependencia.objects.get(id = pk)
    # Verificar el titular y el domicilio de la dependencia si se eliminan
    #titular = dependencia.titular
    #domicilio = dependencia.domicilio
    dependencia.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarDocExpediente(request, pk, file_name):    
    expediente = Expediente.objects.get(id = pk)        
    file_name = file_name.replace('id_', '')    
    archivo = getattr(expediente,file_name)
    archivo.delete()    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarDocR1(request, pk, file_name):
    reporte = ReporteParcial1.objects.get(pk=pk)
    file_name = file_name.replace(' ', '')    
    letter = file_name[0]
    letter = letter.lower()
    file_name = file_name.replace(file_name[0], letter, 1)
    str = 'r1_'
    file_name = str + file_name
    archivo = getattr(reporte,file_name)
    archivo.delete()    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarDocR2(request, pk, file_name):
    reporte = ReporteParcial2.objects.get(pk=pk)
    file_name = file_name.replace(' ', '')    
    letter = file_name[0]
    letter = letter.lower()
    file_name = file_name.replace(file_name[0], letter, 1)
    str = 'r2_'
    file_name = str + file_name
    archivo = getattr(reporte,file_name)
    archivo.delete()    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminarDocRF(request, pk, file_name):
    reporte = ReporteFinal.objects.get(pk=pk)
    file_name = file_name.replace(' ', '')    
    letter = file_name[0]
    letter = letter.lower()
    file_name = file_name.replace(file_name[0], letter, 1)
    str = 'rf_'
    file_name = str + file_name
    archivo = getattr(reporte,file_name)
    archivo.delete()    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def eliminar_aviso(request, pk):
    aviso = Avisos.objects.get(id=pk)
    aviso.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def cancelar_anteproyecto(request, pk):
    estudiante = Estudiante.objects.get(id=pk)
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0]    
    anteproyecto.estado = 'INACTIVO'
    anteproyecto.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@admin_only
def cancelar_residencia(request, pk):
    estudiante = Estudiante.objects.get(id=pk)
    residencia = Estudiante_Residencia.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0]    
    residencia.estado = 'INACTIVO'
    residencia.save()
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0]    
    anteproyecto.estado = 'INACTIVO'
    anteproyecto.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def generar_reportes(request):
    group = request.user.groups.all()[0].name        
    context = {'group': group, 'title': 'Generar Reportes'}
    return render(request, 'Admin/reportes/menu.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def generar_reporte_estudiantes(request, filter1, filter2, filter3, filter4):
    group = request.user.groups.all()[0].name    
    estudiantes = Estudiante.objects.all()      
    generaciones = estudiantes.values(generacion = Substr('numControl', 1, 4)).distinct()
    generaciones = [i['generacion'] for i in generaciones]        
    filtros = [filter1, filter2, filter3, filter4]                        
    estudiantes = MyViewModel.objects.all().order_by('numControl')                                    
    estudiantes, filtros_list = filtrar_estudiantes_rep(estudiantes, filtros)                
    file_name = 'reporte_estudiantes'    
    
    context = {'group': group, 'estudiantes': estudiantes, 'filtros': filtros, 'file_name': file_name, 'filter1': filter1, 'filter2': filter2, 'filter3': filter3, 'filter4': filter4, 'filtros_list': filtros_list, 'generaciones': generaciones, 'title': 'Reporte Estudiantes'}
    return render(request, 'Admin/reportes/estudiantes.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def generar_reporte_anteproyectos(request, filter1, filter2, filter3, filter4, filter5, filter6, filter7, filter8):
    group = request.user.groups.all()[0].name        
    all_anteproyectos = Anteproyecto.objects.all().order_by('-fechaEntrega')
    dependencias = Dependencia.objects.all()   
    filtros = [filter1, filter2, filter3, filter4, filter5, filter6, filter7, filter8]                        
    anteproyectos, filtros_list = filtrar_anteproyectos_rep(all_anteproyectos, filtros)            
    file_name = 'reporte_anteproyectos'    
    context = {'group': group, 'anteproyectos': anteproyectos, 'filtros': filtros, 'file_name': file_name, 'dependencias': dependencias, 'filter1': filter1, 'filter2': filter2, 'filter3': filter3, 'filter4': filter4, 'filter5': filter5, 'filter6': filter6, 'filter7': filter7, 'filter8': filter8, 'filtros_list': filtros_list, 'title': 'Reporte Anteproyectos'}
    return render(request, 'Admin/reportes/anteproyectos.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def generar_reporte_residencias(request, filter1, filter2, filter3, filter4, filter5, filter6, filter7, filter8):
    group = request.user.groups.all()[0].name    
    all_residencias = Residencia.objects.all()
    dependencias = Dependencia.objects.all()   
    filtros = [filter1, filter2, filter3, filter4, filter5, filter6, filter7, filter8]                            
    residencias, filtros_list = filtrar_residencias_rep(all_residencias, filtros)            
    file_name = 'reporte_residencias'        
    context = {'group': group, 'residencias': residencias, 'filtros': filtros, 'file_name': file_name, 'dependencias': dependencias, 'filter1': filter1, 'filter2': filter2, 'filter3': filter3, 'filter4': filter4, 'filter5': filter5, 'filter6': filter6, 'filter7': filter7, 'filter8': filter8, 'filtros_list': filtros_list, 'title': 'Reporte Residencias'}
    return render(request, 'Admin/reportes/residencias.html', context)

@admin_only
def export_excel(request, tipo, name):
    response = HttpResponse(content_type = 'applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename={}.xls'.format(name)
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filtros = request.GET.getlist('my_list')[0]
    filtros = ast.literal_eval(filtros)        
    columns = []
    rows = []
    
    if tipo == 1:                    
        columns = ['Numero de control', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Semestre', 'Nombre anteproyecto' ,'Anteproyecto', 'Residencia', 'Estatus anteproyecto', 'Estatus residencia']    
        all_estudiantes = MyViewModel.objects.all().order_by('numControl')
        estudiantes, filtros_list = filtrar_estudiantes_rep(all_estudiantes, filtros)            
        rows = estudiantes.values_list('numControl', 'nombre', 'apellidoP', 'apellidoM', 'semestre', 'a_nombre', 'anteproyecto_estatus', 'residencia_estatus', 'estado_anteproyecto', 'estado_residencia')    
    elif tipo == 2:
        columns = ['Nombre del anteproyecto', 'Tipo de proyecto', 'Numero de integrantes', 'Fecha de entrega', 'Estatus del anteproyecto', 'Estatus del revisor 1', 'Estatus del revisor 2' , 'Nombre revisor 1', 'Nombre revisor 2', 'Organizacion o empresa']    
        all_anteproyectos = Anteproyecto.objects.annotate(nombre_r1=Concat(F('revisor1__apellidoP'), Value(" "), F("revisor1__apellidoM"), Value(" "), F('revisor1__nombre')), nombre_r2=Concat(F('revisor2__apellidoP'), Value(" "), F("revisor2__apellidoM"), Value(" "), F('revisor2__nombre')))
        anteproyectos, filtros_list = filtrar_anteproyectos_rep(all_anteproyectos, filtros)            
        rows = anteproyectos.values_list('a_nombre', 'tipoProyecto', 'numIntegrantes', 'fechaEntrega', 'estatus', 'estatusR1', 'estatusR2', 'nombre_r1', 'nombre_r2', 'dependencia__d_nombre')    
    elif tipo == 3:
        columns = ['Nombre del proyecto', 'Tipo de proyecto', 'Numero de integrantes', 'Periodo inicio', 'Periodo fin', 'Estatus del proyecto', 'Revisor', 'Asesor interno', 'Asesor externo', 'Organizacion o empresa']    
        all_residencias = Residencia.objects.annotate(nombre_r=Concat(F('r_revisor__apellidoP'), Value(" "), F("r_revisor__apellidoM"), Value(" "), F('r_revisor__nombre')), nombre_asesor_i=Concat(F('r_asesorInterno__apellidoP'), Value(" "), F("r_asesorInterno__apellidoM"), Value(" "), F('r_asesorInterno__nombre')), nombre_asesor_e=Concat(F('asesorExterno__apellidoP'), Value(" "), F("asesorExterno__apellidoM"), Value(" "), F('asesorExterno__nombre')))
        residencias, filtros_list = filtrar_residencias_rep(all_residencias, filtros)            
        rows = residencias.values_list('nombre', 'tipoProyecto', 'numIntegrantes', 'periodoInicio', 'periodoFin', 'estatus', 'nombre_r', 'nombre_asesor_i', 'nombre_asesor_e', 'dependencia__d_nombre')    
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()                            
            
    for row in rows:        
        row_num += 1        
        for col_num in range(len(row)):            
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)
    
    return response    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def estudiantes_autorizados(request, page, filter1, filter2):
    group = request.user.groups.all()[0].name    
    all_estudiantes = Estudiante_Autorizado.objects.all()
    start = (page-1)*10    
    end = page*10              
    filtros = [filter1, filter2]
    generaciones = all_estudiantes.values(generacion = Substr('num_control', 1, 4)).distinct()
    generaciones = [i['generacion'] for i in generaciones]        
    all_estudiantes = filtrar_estudiantes_aut(all_estudiantes, filtros)    
    estudiantes = all_estudiantes[start:end]
    
    if end != estudiantes.count():
        end = end-10+estudiantes.count()
    totalE = all_estudiantes.count()
    n_buttons = math.ceil(totalE/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    context = {'group': group, 'estudiantes': estudiantes, 'generaciones': generaciones, 'page': page, 'start': start+1, 'end': end, 'totalE': totalE, 'n_buttons': n_buttons, 'buttons': buttons, 'next_page': next_page, 'prev_page': prev_page, 'filter1': filter1, 'filter2': filter2, 'title': 'Estudiantes Autorizados'}
    return render(request, 'Admin/estudiantes_autorizados/estudiantes.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def subir_estudiantes_a(request):    
    group = request.user.groups.all()[0].name    
    form = CSVUploadForm()
    
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)        
        if form.is_valid():
            file = form.cleaned_data['csv_file']            
            data = file.read().decode('utf-8')
            lines = data.split("\n")
            reader = csv.reader(lines)
            for row in reader:
                try:
                    estudiante_a = Estudiante_Autorizado.objects.create(num_control=row[0], nombre_completo=row[1])                                        
                except:
                    pass                
            return redirect('estudiantes_autorizados' ,1, 0, 0)
    
    context = {'group': group, 'form': form, 'title': 'Subir Estudiantes'}
    return render(request, 'Admin/estudiantes_autorizados/subir_documento.html', context)

def convert_to_pdf(request, context, template_path):
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def export_pdf(request, tipo, name):
    filtros = request.GET.getlist('my_list2')[0]
    filtros = ast.literal_eval(filtros)
    fecha_actual = datetime.now()
    if tipo == 1:                    
        columns = ['Numero de control', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Semestre', 'Nombre anteproyecto' ,'Anteproyecto', 'Residencia', 'Estatus anteproyecto', 'Estatus residencia']    
        all_estudiantes = MyViewModel.objects.all().order_by('numControl')
        estudiantes, filtros_list = filtrar_estudiantes_rep(all_estudiantes, filtros)           
        datos_t = len(estudiantes)         
        context = {'estudiantes': estudiantes, 'fecha_actual': fecha_actual, 'datos_t': datos_t}
        template_path = 'Admin/reportes/PDF/pdf_estudiantes.html'
    elif tipo == 2:
        columns = ['Nombre del anteproyecto', 'Tipo de proyecto', 'Numero de integrantes', 'Fecha de entrega', 'Estatus del anteproyecto', 'Estatus del revisor 1', 'Estatus del revisor 2' , 'Nombre revisor 1', 'Nombre revisor 2', 'Organizacion o empresa']    
        all_anteproyectos = Anteproyecto.objects.annotate(nombre_r1=Concat(F('revisor1__apellidoP'), Value(" "), F("revisor1__apellidoM"), Value(" "), F('revisor1__nombre')), nombre_r2=Concat(F('revisor2__apellidoP'), Value(" "), F("revisor2__apellidoM"), Value(" "), F('revisor2__nombre')))
        anteproyectos, filtros_list = filtrar_anteproyectos_rep(all_anteproyectos, filtros)                    
        datos_t = len(anteproyectos)        
        context = {'anteproyectos': anteproyectos, 'fecha_actual': fecha_actual, 'datos_t': datos_t}
        template_path = 'Admin/reportes/PDF/pdf_anteproyectos.html'    
    elif tipo == 3:
        columns = ['Nombre del proyecto', 'Tipo de proyecto', 'Numero de integrantes', 'Periodo inicio', 'Periodo fin', 'Estatus del proyecto', 'Revisor', 'Asesor interno', 'Asesor externo', 'Organizacion o empresa']    
        all_residencias = Residencia.objects.annotate(nombre_r=Concat(F('r_revisor__apellidoP'), Value(" "), F("r_revisor__apellidoM"), Value(" "), F('r_revisor__nombre')), nombre_asesor_i=Concat(F('r_asesorInterno__apellidoP'), Value(" "), F("r_asesorInterno__apellidoM"), Value(" "), F('r_asesorInterno__nombre')), nombre_asesor_e=Concat(F('asesorExterno__apellidoP'), Value(" "), F("asesorExterno__apellidoM"), Value(" "), F('asesorExterno__nombre')))
        residencias, filtros_list = filtrar_residencias_rep(all_residencias, filtros)                    
        datos_t = len(residencias)        
        context = {'residencias': residencias, 'fecha_actual': fecha_actual, 'datos_t': datos_t}
        template_path = 'Admin/reportes/PDF/pdf_residencias.html'    
                    
    pdf = convert_to_pdf(request, context, template_path)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = name
        #filename = "Invoice_%s.pdf" %("12341231")
        content = "inline; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def act_docente_anteproyectosA(request, pk):
    group = request.user.groups.all()[0].name
    docente = Docente.objects.get(id=pk)
    estados = ['ACEPTADO', 'RECHAZADO', 'CANCELADO']
    all_anteproyectosR1 = Anteproyecto.objects.filter(revisor1=docente).exclude(estatus__in=estados).order_by('fechaEntrega')
    all_anteproyectosR2 = Anteproyecto.objects.filter(revisor2=docente).exclude(estatus__in=estados).order_by('fechaEntrega')            
    
    context = {'group': group, 'all_anteproyectosR1': all_anteproyectosR1, 'all_anteproyectosR2': all_anteproyectosR2, 'docente': docente, 'title': 'Anteproyectos Activos'}    
    return render(request, 'Admin/actividad_docente/actividad_anteproyectosA.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def act_docente_anteproyectosH(request, pk, page1, page2, orderB1, orderB2, filter1, filter2):
    group = request.user.groups.all()[0].name
    docente = Docente.objects.get(id=pk)
    estados = ['ACEPTADO', 'RECHAZADO', 'CANCELADO']
    all_anteproyectosR1 = Anteproyecto.objects.filter(revisor1=docente, estatus__in=estados)
    all_anteproyectosR2 = Anteproyecto.objects.filter(revisor2=docente, estatus__in=estados)
    
    start1 = (page1-1)*10    
    end1 = page1*10
    
    start2 = (page2-1)*10    
    end2 = page2*10
    
    all_anteproyectosR1 = filtrar_anteproyectos(all_anteproyectosR1, filter1)
    all_anteproyectosR1 = ordenar_anteproyectos(all_anteproyectosR1, orderB1)
    all_anteproyectosR1 = all_anteproyectosR1[start1:end1]    
    if end1 != all_anteproyectosR1.count():
        end1 = end1-10+all_anteproyectosR1.count()
    totalA1 = all_anteproyectosR1.count()
    n_buttons1 = math.ceil(totalA1/10)
    buttons1 = [item for item in range(1, n_buttons1+1)]
    next_page1 = page1+1
    prev_page1 = page1-1    
    
    all_anteproyectosR2 = filtrar_anteproyectos(all_anteproyectosR2, filter2)
    all_anteproyectosR2 = ordenar_anteproyectos(all_anteproyectosR2, orderB2)
    all_anteproyectosR2 = all_anteproyectosR2[start2:end2]  
    if end2 != all_anteproyectosR2.count():
        end2 = end2-10+all_anteproyectosR2.count()  
    totalA2 = all_anteproyectosR2.count()
    n_buttons2 = math.ceil(totalA2/10)
    buttons2 = [item for item in range(1, n_buttons2+1)]
    next_page2 = page2+1
    prev_page2 = page2-1        
    
        
    context = {'group': group, 'all_anteproyectosR1': all_anteproyectosR1, 'all_anteproyectosR2': all_anteproyectosR2, 'totalA1': totalA1, 'totalA2': totalA2, 'buttons1': buttons1, 'buttons2': buttons2, 'page1': page1, 'page2': page2, 'start1': start1+1, 'start2': start2+1, 'end1': end1, 'end2': end2, 'next_page1': next_page1, 'next_page2': next_page2, 'prev_page1': prev_page1, 'prev_page2': prev_page2, 'n_buttons1': n_buttons1, 'n_buttons2': n_buttons2, 'orderB1': orderB1, 'orderB2': orderB2, 'filter1': filter1, 'filter2': filter2, 'docente': docente, 'title': 'Anteproyectos Historicos'}    
    return render(request, 'Admin/actividad_docente/actividad_anteproyectosH.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def act_docente_residenciasA(request, pk):
    group = request.user.groups.all()[0].name
    docente = Docente.objects.get(id=pk)
    estados = ['FINALIZADA', 'RECHAZADA', 'NO FINALIZADA', 'CANCELADA']
    all_residenciasA = Residencia.objects.filter(r_asesorInterno=docente).exclude(estatus__in=estados)
    all_residenciasR = Residencia.objects.filter(r_revisor=docente).exclude(estatus__in=estados)            
    
    context = {'group': group, 'all_residenciasA': all_residenciasA, 'all_residenciasR': all_residenciasR, 'docente': docente, 'title': 'Residencias Activas'}    
    return render(request, 'Admin/actividad_docente/actividad_residenciasA.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_only
def act_docente_residenciasH(request, pk, page1, page2, orderB1, orderB2, filter1, filter2):
    group = request.user.groups.all()[0].name
    docente = Docente.objects.get(id=pk)
    estados = ['RECHAZADA', 'NO FINALIZADA', 'FINALIZADA', 'CANCELADA']
    
    all_residenciasA = Residencia.objects.filter(r_asesorInterno=docente, estatus__in=estados)
    all_residenciasR = Residencia.objects.filter(r_revisor=docente, estatus__in=estados)        
    
    start1 = (page1-1)*10    
    end1 = page1*10
    
    start2 = (page2-1)*10    
    end2 = page2*10
    
    all_residenciasA = filtrar_residencias(all_residenciasA, filter1)
    all_residenciasA = ordenar_residencias(all_residenciasA, orderB1)
    all_residenciasA = all_residenciasA[start1:end1]    
    if end1 != all_residenciasA.count():
        end1 = end1-10+all_residenciasA.count()
    totalR1 = all_residenciasA.count()
    n_buttons1 = math.ceil(totalR1/10)
    buttons1 = [item for item in range(1, n_buttons1+1)]
    next_page1 = page1+1
    prev_page1 = page1-1   
    
    all_residenciasR = filtrar_residencias(all_residenciasR, filter1)
    all_residenciasR = ordenar_residencias(all_residenciasR, orderB1)
    all_residenciasR = all_residenciasR[start2:end2]    
    if end2 != all_residenciasR.count():
        end2 = end2-10+all_residenciasR.count()
    totalR2 = all_residenciasR.count()
    n_buttons2 = math.ceil(totalR2/10)
    buttons2 = [item for item in range(1, n_buttons2+1)]
    next_page2 = page2+1
    prev_page2 = page2-1   
    
    context = {'group': group, 'all_residenciasA': all_residenciasA, 'all_residenciasR': all_residenciasR, 'totalR1': totalR1, 'totalR2': totalR2, 'buttons1': buttons1, 'buttons2': buttons2, 'page1': page1, 'page2': page2, 'start1': start1+1, 'start2': start2+1, 'end1': end1, 'end2': end2, 'next_page1': next_page1, 'next_page2': next_page2, 'prev_page1': prev_page1, 'prev_page2': prev_page2, 'n_buttons1': n_buttons1, 'n_buttons2': n_buttons2, 'orderB1': orderB1, 'orderB2': orderB2, 'filter1': filter1, 'filter2': filter2, 'docente': docente, 'title': 'Residencias Historicas'}    
    return render(request, 'Admin/actividad_docente/actividad_residenciasH.html', context)

def filtrar_anteproyectos(anteproyectos, filter):
    all_anteproyectos = anteproyectos
    if filter == 1:
        all_anteproyectos = anteproyectos.filter(estatus = 'ACEPTADO')
    elif filter == 2:
        all_anteproyectos = anteproyectos.filter(estatus = 'ENVIADO')
    elif filter == 3:
        all_anteproyectos = anteproyectos.filter(estatus = 'PENDIENTE')
    elif filter == 4:
        all_anteproyectos = anteproyectos.filter(estatus = 'EN REVISION')
    elif filter == 5:
        all_anteproyectos = anteproyectos.filter(estatus = 'REVISADO')
    elif filter == 6:
        all_anteproyectos = anteproyectos.filter(estatus = 'CANCELADO')
    elif filter == 7:
        all_anteproyectos = anteproyectos.filter(estatus = 'RECHAZADO')
    return all_anteproyectos

def ordenar_anteproyectos(anteproyectos, orderB):
    all_anteproyectos = anteproyectos           
    if orderB == 1:
        all_anteproyectos = all_anteproyectos.order_by('a_nombre')    
    elif orderB == 2:
        all_anteproyectos = all_anteproyectos.order_by('-a_nombre')        
    elif orderB == 3:
        all_anteproyectos = all_anteproyectos.order_by('-fechaEntrega')    
    elif orderB == 4:
        all_anteproyectos = all_anteproyectos.order_by('fechaEntrega')    
    
    return all_anteproyectos

def buscar_anteproyecto(anteproyectos, text, opc):
    all_anteproyectos = anteproyectos
    if opc == 1:                
        all_anteproyectos = all_anteproyectos.filter(a_nombre__icontains=text)
    elif opc == 2:                
        dependencias = Dependencia.objects.filter(d_nombre__icontains=text)
        all_anteproyectos = all_anteproyectos.filter(dependencia__in=dependencias)
    elif opc == 3:                
        try:
            month_number = int(text)
            if month_number > 0 and month_number <= 12:                        
                all_anteproyectos = all_anteproyectos.filter(fechaEntrega__month=month_number)                                                   
            else:
                month_number = None
                all_anteproyectos = all_anteproyectos.filter(fechaEntrega__month=month_number)                                                   
        except:                    
            MONTHS = {'ENERO':1, 'FEBRERO':2, 'MARZO':3, 'ABRIL':4, 'MAYO':5, 'JUNIO':6, 'JULIO':7, 'AGOSTO':8, 'SEPTIEMBRE':9, 'OCTUBRE':10, 'NOVIEMBRE':11, 'DICIEMBRE':12}                                                
            try:
                text = text.upper()
                month_number = MONTHS[text]
                all_anteproyectos = all_anteproyectos.filter(fechaEntrega__month=month_number)                                                   
            except:
                month_number = None
                all_anteproyectos = all_anteproyectos.filter(fechaEntrega__month=month_number)                                                                                       
    elif opc == 4:
        try:
            year = int(text) 
            all_anteproyectos = all_anteproyectos.filter(fechaEntrega__year=year)                               
        except:
            text = None                
    elif opc == 5:                
        try:
            year = int(text) 
            all_anteproyectos = all_anteproyectos.filter(fechaEntrega__year=year)                               
        except:
            text = None                           
    
    return all_anteproyectos 

def filtrar_residencias(residencias, filter):
    all_residencias = residencias
    if filter == 1:
        all_residencias = all_residencias.filter(estatus = 'INICIADA')
    elif filter == 2:
        all_residencias = all_residencias.filter(estatus = 'FINALIZADA')
    elif filter == 3:
        all_residencias = all_residencias.filter(estatus = 'EN PROCESO')
    elif filter == 4:
        all_residencias = all_residencias.filter(estatus = 'CANCELADA')
    elif filter == 5:
        all_residencias = all_residencias.filter(estatus = 'RECHAZADA')
    elif filter == 6:
        all_residencias = all_residencias.filter(estatus = 'PROROGA')    
    return all_residencias

def ordenar_residencias(residencias, orderB):
    all_residencias = residencias
    if orderB == 1:
        all_residencias = all_residencias.order_by('nombre')    
    elif orderB == 2:
        all_residencias = all_residencias.order_by('-nombre')        
    elif orderB == 3:
        all_residencias = all_residencias.order_by('periodoInicio')    
    elif orderB == 4:
        all_residencias = all_residencias.order_by('-periodoInicio')    
    elif orderB == 5:
        all_residencias = all_residencias.order_by('periodoFin')    
    elif orderB == 6:
        all_residencias = all_residencias.order_by('-periodoFin')        
    return all_residencias

def buscar_residencia(residencias, text, opc):
    all_residencias = residencias
    if opc == 1:                
        all_residencias = all_residencias.filter(nombre__icontains=text)
    elif opc == 2:                
        dependencias = Dependencia.objects.filter(d_nombre__icontains=text)
        all_residencias = all_residencias.filter(dependencia__in=dependencias)
    elif opc == 3:                
        try:
            month_number = int(text)
            if month_number > 0 and month_number <= 12:                        
                all_residencias = all_residencias.filter(periodoInicio__month=month_number)                                                   
            else:
                month_number = None
                all_residencias = all_residencias.filter(periodoInicio__month=month_number)                                                   
        except:                    
            MONTHS = {'ENERO':1, 'FEBRERO':2, 'MARZO':3, 'ABRIL':4, 'MAYO':5, 'JUNIO':6, 'JULIO':7, 'AGOSTO':8, 'SEPTIEMBRE':9, 'OCTUBRE':10, 'NOVIEMBRE':11, 'DICIEMBRE':12}                                                
            try:
                text = text.upper()
                month_number = MONTHS[text]
                all_residencias = all_residencias.filter(periodoInicio__month=month_number)                                                   
            except:
                month_number = None
                all_residencias = all_residencias.filter(periodoInicio__month=month_number)                                                   

    elif opc == 4:
        try:
            month_number = int(text)
            if month_number > 0 and month_number <= 12:                        
                all_residencias = all_residencias.filter(periodoFin__month=month_number)                                                   
            else:
                month_number = None
                all_residencias = all_residencias.filter(periodoFin__month=month_number)                                                   
        except:                    
            MONTHS = {'ENERO':1, 'FEBRERO':2, 'MARZO':3, 'ABRIL':4, 'MAYO':5, 'JUNIO':6, 'JULIO':7, 'AGOSTO':8, 'SEPTIEMBRE':9, 'OCTUBRE':10, 'NOVIEMBRE':11, 'DICIEMBRE':12}                                                
            try:
                text = text.upper()
                month_number = MONTHS[text]
                all_residencias = all_residencias.filter(periodoFin__month=month_number)                                                   
            except:
                month_number = None
                all_residencias = all_residencias.filter(periodoFin__month=month_number)                                                   

    elif opc == 5:                
        try:
            year = int(text) 
            all_residencias = all_residencias.filter(periodoInicio__year=year)                               
        except:
            year = None     
            all_residencias = all_residencias.filter(periodoInicio__year=year)                                          
    elif opc == 6:       
        try:
            year = int(text) 
            all_residencias = all_residencias.filter(periodoFin__year=year)                               
        except:
            year = None         
            all_residencias = all_residencias.filter(periodoFin__year=year)                                                                  
    return all_residencias

def filtrar_expedientes(estudiantes, filter):
    all_expedientes = Expediente.objects.all()
    all_estudiantes = estudiantes        
    if filter == 1:
        all_expedientes = all_expedientes.filter(estatus = 'INICIAL')
    elif filter == 2:
        all_expedientes = all_expedientes.filter(estatus = 'PROCESO')
    elif filter == 3:
        all_expedientes = all_expedientes.filter(estatus = 'COMPLETO')        
    elif filter == 4:
        all_expedientes = all_expedientes.filter(estatus = 'FINALIZADO')        
    all_estudiantes = all_estudiantes.filter(expediente__in = all_expedientes)    
    return all_estudiantes

def ordenar_estudiantes(estudiantes, orderB):
    all_estudiantes = estudiantes                
    if orderB == 1:
        all_estudiantes = all_estudiantes.order_by('semestre')    
    elif orderB == 2:
        all_estudiantes = all_estudiantes.order_by('-semestre')    
    elif orderB == 3:
        all_estudiantes = all_estudiantes.order_by('numControl')        
    elif orderB == 4:
        all_estudiantes = all_estudiantes.order_by('-numControl')    
    elif orderB == 5:
        all_estudiantes = all_estudiantes.order_by('apellidoP')    
    elif orderB == 6:
        all_estudiantes = all_estudiantes.order_by('-apellidoP')    
    else:
        all_estudiantes = all_estudiantes          
    return all_estudiantes
    
def buscar_estudiante(estudiantes ,text, opc):
    all_estudiantes = estudiantes    
    if text:
        if opc == 1:                
            all_estudiantes = all_estudiantes.filter(numControl__icontains=text)
        elif opc == 2:                
            all_estudiantes = all_estudiantes.filter(nombre__icontains=text)
        elif opc == 3:                
            all_estudiantes = all_estudiantes.filter(apellidoP__icontains=text)
        elif opc == 4:
            all_estudiantes = all_estudiantes.filter(apellidoM__icontains=text)
        elif opc == 5:
            all_estudiantes = all_estudiantes.filter(correoElectronico__icontains=text)
        elif opc == 6: 
            try:               
                all_estudiantes = all_estudiantes.filter(semestre=text)
            except: 
                all_estudiantes = all_estudiantes.filter(semestre=None)
    
    return all_estudiantes

def ordenar_docentes(docentes, orderB):
    all_docentes = docentes
    if orderB == 1:
        all_docentes = all_docentes.order_by('nombre')    
    elif orderB == 2:
        all_docentes = all_docentes.order_by('-nombre')    
    elif orderB == 3:
        all_docentes = all_docentes.order_by('apellidoP')        
    elif orderB == 4:
        all_docentes = all_docentes.order_by('-apellidoP')    
    elif orderB == 5:
        all_docentes = all_docentes.order_by('rfc')    
    elif orderB == 6:
        all_docentes = all_docentes.order_by('-rfc')        
    return all_docentes

def buscar_docente(docentes, text, opc):    
    all_docentes = docentes
    if opc == 1:                
        all_docentes = all_docentes.filter(nombre__icontains=text)            
    elif opc == 2:                
        all_docentes = all_docentes.filter(apellidoP__icontains=text)
    elif opc == 3:
        all_docentes = all_docentes.filter(apellidoM__icontains=text)            
    elif opc == 4:
        all_docentes = all_docentes.filter(rfc__icontains=text)            
        
    return all_docentes

def ordenar_materias(materias, orderB):
    all_materias = materias
    if orderB == 1:
        all_materias = all_materias.order_by('nombre')    
    elif orderB == 2:
        all_materias = all_materias.order_by('-nombre')    
    elif orderB == 3:
        all_materias = all_materias.order_by('semestre')        
    elif orderB == 4:
        all_materias = all_materias.order_by('-semestre')        
    return all_materias

def buscar_materia(materias, text, opc):    
    all_materias = materias
    if opc == 1:                
        all_materias = all_materias.filter(clave__icontains=text)            
    elif opc == 2:                
        all_materias = all_materias.filter(nombre__icontains=text)
    elif opc == 3:
        all_materias = all_materias.filter(semestre__icontains=text)                        
    return all_materias

def filtrar_materias(materias, filter):    
    all_materias = materias        
    
    if filter == 1:
        all_materias = all_materias.filter(semestre = 1)
    elif filter == 2:
        all_materias = all_materias.filter(semestre = 2)
    elif filter == 3:
        all_materias = all_materias.filter(semestre = 3)        
    elif filter == 4:
        all_materias = all_materias.filter(semestre = 4)        
    elif filter == 5:
        all_materias = all_materias.filter(semestre = 5)        
    elif filter == 6:
        all_materias = all_materias.filter(semestre = 6)        
    elif filter == 7:
        all_materias = all_materias.filter(semestre = 7)        
    elif filter == 8:
        all_materias = all_materias.filter(semestre = 8)        
    elif filter == 9:
        all_materias = all_materias.filter(semestre = 9)        
            
    return all_materias

def ordenar_dependencias(dependencias, orderB):
    all_dependencias = dependencias
    if orderB == 1:
        all_dependencias = all_dependencias.order_by('d_nombre')    
    elif orderB == 2:
        all_dependencias = all_dependencias.order_by('-d_nombre')        
    return all_dependencias

def buscar_dependencia(dependencias, text, opc):    
    all_dependencias = dependencias
    if opc == 1:                
        all_dependencias = all_dependencias.filter(d_nombre__icontains=text)            
    elif opc == 2:                
        all_dependencias = all_dependencias.filter(rfc__icontains=text)    
    return all_dependencias

def filtrar_dependencias(dependencias, filter):    
    all_dependencias = dependencias       
    
    if filter == 1:
        all_dependencias = all_dependencias.filter(giro = 'INDUSTRIAL')
    elif filter == 2:
        all_dependencias = all_dependencias.filter(giro = 'SERVICIOS')
    elif filter == 3:
        all_dependencias = all_dependencias.filter(giro = 'PUBLICO')        
    elif filter == 4:
        all_dependencias = all_dependencias.filter(giro = 'PRIVADO')            
            
    return all_dependencias

def filtrar_estudiantes_rep(all_estudiantes, filtros):
    estudiantes = all_estudiantes
    filtros_list = []
            
    filtro1 = filtros[0]
    filtro2 = filtros[1]
    filtro3 = filtros[2]
    filtro4 = filtros[3]    
    
    if filtro1 == 9:
        estudiantes = estudiantes.filter(semestre = 9)
        filtros_list.append('Semestre 9')
    elif filtro1 == 10:
        estudiantes = estudiantes.filter(semestre = 10)
        filtros_list.append('Semestre 10')
    elif filtro1 == 11:
        estudiantes = estudiantes.filter(semestre = 11)
        filtros_list.append('Semestre 11')
    elif filtro1 == 12:
        estudiantes = estudiantes.filter(semestre = 12)
        filtros_list.append('Semestre 12')
    elif filtro1 == 13:
        estudiantes = estudiantes.filter(semestre = 13)
        filtros_list.append('Semestre 13')
    elif filtro1 == 14:
        estudiantes = estudiantes.filter(semestre = 14)
        filtros_list.append('Semestre 14')
    elif filtro1 == 15:
        estudiantes = estudiantes.filter(semestre = 14)
        filtros_list.append('Semestre 14')
        
    if filtro2 != '0':        
        filtros_list.append(f'Numero de control: {filtro2}')
        estudiantes = estudiantes.filter(numControl__startswith = filtro2)
    
    if filtro3 == 1:  
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'ENVIADO')              
        filtros_list.append('Anteproyecto ENVIADO')
    elif filtro3 == 2:        
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'PENDIENTE')                      
        filtros_list.append('Anteproyecto PENDIENTE')
    elif filtro3 == 3:   
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'EN REVISION')                           
        filtros_list.append('Anteproyecto EN REVISION')
    elif filtro3 == 4:  
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'REVISADO')                                    
        filtros_list.append('Anteproyecto REVISADO')
    elif filtro3 == 5:     
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'ACEPTADO')                         
        filtros_list.append('Anteproyecto ACEPTADO')
    elif filtro3 == 6:    
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'RECHAZADO')                          
        filtros_list.append('Anteproyecto RECHAZADO')
    elif filtro3 == 7:  
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'CANCELADO')                            
        filtros_list.append('Anteproyecto CANCELADO')
    elif filtro3 == 8:
        estudiantes = estudiantes.filter(anteproyecto_estatus = 'SIN ENVIO')                              
        filtros_list.append('Anteproyecto SIN ENVIO')
        
    if filtro4 == 1:   
        estudiantes = estudiantes.filter(residencia_estatus = 'INICIADA')                           
        filtros_list.append('Residencia INICIADA')
    elif filtro4 == 2:   
        estudiantes = estudiantes.filter(residencia_estatus = 'EN PROCESO')                                
        filtros_list.append('Residencia EN PROCESO')
    elif filtro4 == 3:   
        estudiantes = estudiantes.filter(residencia_estatus = 'PRORROGA')                                
        filtros_list.append('Residencia PRORROGA')
    elif filtro4 == 4:      
        estudiantes = estudiantes.filter(residencia_estatus = 'NO FINALIZADA')                             
        filtros_list.append('Residencia NO FINALIZADA')
    elif filtro4 == 5:        
        estudiantes = estudiantes.filter(residencia_estatus = 'RECHAZADA')                           
        filtros_list.append('Residencia RECHAZADA')
    elif filtro4 == 6:      
        estudiantes = estudiantes.filter(residencia_estatus = 'FINALIZADA')                             
        filtros_list.append('Residencia FINALIZADA')
    elif filtro4 == 7:      
        estudiantes = estudiantes.filter(residencia_estatus = 'CANCELADA')                             
        filtros_list.append('Residencia CANCELADA')
    elif filtro4 == 8:        
        estudiantes = estudiantes.filter(residencia_estatus = 'SIN ENVIO')                           
        filtros_list.append('Residencia SIN ENVIO')
        
    return estudiantes, filtros_list

def filtrar_anteproyectos_rep(all_anteproyectos, filtros):
    anteproyectos = all_anteproyectos
    filtros_list = []
            
    filtro1 = filtros[0]
    filtro2 = filtros[1]
    filtro3 = filtros[2]
    filtro4 = filtros[3]
    filtro5 = filtros[4]
    filtro6 = filtros[5]
    filtro7 = filtros[6]
    filtro8 = filtros[7]
    
    fecha_de = filtro3
    fecha_hasta = filtro4       
    
    try:        
        fecha_de_obj = datetime.strptime(fecha_de, '%Y-%m-%d').date()    
    except:
        fecha_de_obj = None
        
    try:        
        fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()    
    except:
        fecha_hasta_obj = None
            
    if filtro1 == 1:
        anteproyectos = anteproyectos.exclude(estatus__in = ['ACEPTADO', 'RECHAZADO', 'CANCELADO'])
        filtros_list.append('Anteproyectos ACTIVOS')
    elif filtro1 == 2:
        anteproyectos = anteproyectos.filter(estatus__in = ['ACEPTADO', 'RECHAZADO', 'CANCELADO'])
        filtros_list.append('Anteproyectos HISTORICOS')                
    
    if filtro2 == 1:
        anteproyectos = anteproyectos.filter(tipoProyecto = 'PROPUESTA PROPIA')
        filtros_list.append('Tipo proyecto PROPUESTA PROPIA')
    elif filtro2 == 2:
        anteproyectos = anteproyectos.filter(tipoProyecto = 'BANCO DE PROYECTOS')
        filtros_list.append('Tipo proyecto BANCO DE PROYECTOS')
    elif filtro2 == 3:
        anteproyectos = anteproyectos.filter(tipoProyecto = 'TRABAJADOR')
        filtros_list.append('Tipo proyecto TRABAJADOR')
        
    if fecha_de_obj:                
        if fecha_hasta_obj:             
            anteproyectos = anteproyectos.filter(fechaEntrega__range=(fecha_de_obj, fecha_hasta_obj))                        
            date_time_str1 = fecha_de_obj.strftime("%d - %b - %Y")
            date_time_str2 = fecha_hasta_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Anteproyectos entregados a partir de {date_time_str1} hasta {date_time_str2}')
        else:
            anteproyectos = anteproyectos.filter(fechaEntrega__gte=fecha_de_obj)        
            date_time_str = fecha_de_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Anteproyectos entregados a partir de: {date_time_str}')
            
    if fecha_hasta_obj:        
        if not fecha_de_obj:                         
            anteproyectos = anteproyectos.filter(fechaEntrega__lte=fecha_hasta_obj)
            date_time_str = fecha_hasta_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Anteproyectos entregados hasta: {date_time_str}')                            
    
    if filtro5 == 1:
        anteproyectos = anteproyectos.filter(estatus = 'ENVIADO')
        filtros_list.append('Anteproyecto ENVIADO')
    elif filtro5 == 2:
        anteproyectos = anteproyectos.filter(estatus = 'PENDIENTE')
        filtros_list.append('Anteproyecto PENDIENTE')
    elif filtro5 == 3:
        anteproyectos = anteproyectos.filter(estatus = 'EN REVISION')
        filtros_list.append('Anteproyecto EN REVISION')
    elif filtro5 == 4:
        anteproyectos = anteproyectos.filter(estatus = 'REVISADO')
        filtros_list.append('Anteproyecto REVISADO')
    elif filtro5 == 5:
        anteproyectos = anteproyectos.filter(estatus = 'ACEPTADO')
        filtros_list.append('Anteproyecto ACEPTADO')
    elif filtro5 == 6:
        anteproyectos = anteproyectos.filter(estatus = 'RECHAZADO')
        filtros_list.append('Anteproyecto RECHAZADO')
    elif filtro5 == 7:
        anteproyectos = anteproyectos.filter(estatus = 'CANCELADO')
        filtros_list.append('Anteproyecto CANCELADO')
    
    if filtro6 == 1:
        anteproyectos = anteproyectos.filter(estatusR1 = 'PENDIENTE')
        filtros_list.append('Revisor 1 PENDIENTE')
    elif filtro6 == 2:
        anteproyectos = anteproyectos.filter(estatusR1 = 'EN REVISION')
        filtros_list.append('Revisor 1 EN REVISION')
    elif filtro6 == 3:
        anteproyectos = anteproyectos.filter(estatusR1 = 'ACEPTADO')
        filtros_list.append('Revisor 1 ACEPTADO')
    elif filtro6 == 4:
        anteproyectos = anteproyectos.filter(estatusR1 = 'RECHAZADO')
        filtros_list.append('Revisor 1 RECHAZADO')    
        
    if filtro7 == 1:
        anteproyectos = anteproyectos.filter(estatusR2 = 'PENDIENTE')
        filtros_list.append('Revisor 2 PENDIENTE')
    elif filtro7 == 2:
        anteproyectos = anteproyectos.filter(estatusR2 = 'EN REVISION')
        filtros_list.append('Revisor 2 EN REVISION')
    elif filtro7 == 3:
        anteproyectos = anteproyectos.filter(estatusR2 = 'ACEPTADO')
        filtros_list.append('Revisor 2 ACEPTADO')
    elif filtro7 == 4:
        anteproyectos = anteproyectos.filter(estatusR2 = 'RECHAZADO')
        filtros_list.append('Revisor 2 RECHAZADO')    
    
    if filtro8 == '1':        
        anteproyectos = anteproyectos.filter(dependencia__isnull = True)
        filtros_list.append('Sin organizacion o empresa')    
    elif filtro8 == '2':        
        anteproyectos = anteproyectos.filter(dependencia__isnull = False)
        filtros_list.append('Con organizacion o empresa')    
    elif filtro8 != '0':
        dependencia = Dependencia.objects.get(id = filtro8)
        anteproyectos = anteproyectos.filter(dependencia = dependencia)
        filtros_list.append(f'Organizacion o empresa: {dependencia.d_nombre}')    
    
    return anteproyectos, filtros_list

def filtrar_residencias_rep(all_residencias, filtros):
    residencias = all_residencias
    filtros_list = []
    filtro1 = filtros[0]
    filtro2 = filtros[1]
    filtro3 = filtros[2]
    filtro4 = filtros[3]
    filtro5 = filtros[4]
    filtro6 = filtros[5]
    filtro7 = filtros[6]
    filtro8 = filtros[7]
    
    periodo_inicio_de = filtro5
    periodo_inicio_hasta = filtro6       
    
    periodo_fin_de = filtro7
    periodo_fin_hasta = filtro8       
    
    try:        
        periodo_inicio_de_obj = datetime.strptime(periodo_inicio_de, '%Y-%m-%d').date()    
    except:
        periodo_inicio_de_obj = None
        
    try:        
        periodo_inicio_hasta_obj = datetime.strptime(periodo_inicio_hasta, '%Y-%m-%d').date()    
    except:
        periodo_inicio_hasta_obj = None
        
    try:        
        periodo_fin_de_obj = datetime.strptime(periodo_fin_de, '%Y-%m-%d').date()    
    except:
        periodo_fin_de_obj = None
        
    try:        
        periodo_fin_hasta_obj = datetime.strptime(periodo_fin_hasta, '%Y-%m-%d').date()    
    except:
        periodo_fin_hasta_obj = None
    
    if filtro1 == 1:
        residencias = residencias.exclude(estatus__in = ['NO FINALIZADA', 'RECHAZADA', 'FINALIZADA', 'CANCELADA'])
        filtros_list.append('Residencias ACTIVAS')
    elif filtro1 == 2:
        residencias = residencias.filter(estatus__in = ['NO FINALIZADA', 'RECHAZADA', 'FINALIZADA', 'CANCELADA'])
        filtros_list.append('Residencias HISTORICAS')
    
    if filtro2 == 1:
        residencias = residencias.filter(tipoProyecto = 'PROPUESTA PROPIA')
        filtros_list.append('Tipo Proyecto PROPUESTA PROPIA')
    elif filtro2 == 2:
        residencias = residencias.filter(tipoProyecto = 'BANCO DE PROYECTOS')
        filtros_list.append('Tipo Proyecto BANCO DE PROYECTOS')
    elif filtro2 == 3:
        residencias = residencias.filter(tipoProyecto = 'TRABAJADOR')
        filtros_list.append('Tipo Proyecto TRABAJADOR')
        
    if filtro3 == 1:
        residencias = residencias.filter(estatus = 'INICIADA')
        filtros_list.append('Residencias INICIADA')
    elif filtro3 == 2:
        residencias = residencias.filter(estatus = 'EN PROCESO')
        filtros_list.append('Residencias EN PROCESO')
    elif filtro3 == 3:
        residencias = residencias.filter(estatus = 'PRORROGA')
        filtros_list.append('Residencias PRORROGA')
    elif filtro3 == 4:
        residencias = residencias.filter(estatus = 'NO FINALIZADA')
        filtros_list.append('Residencias NO FINALIZADA')
    elif filtro3 == 5:
        residencias = residencias.filter(estatus = 'RECHAZADA')
        filtros_list.append('Residencias RECHAZADA')
    elif filtro3 == 6:
        residencias = residencias.filter(estatus = 'FINALIZADA')
        filtros_list.append('Residencias FINALIZADA')
    elif filtro3 == 7:
        residencias = residencias.filter(estatus = 'CANCELADA')
        filtros_list.append('Residencias CANCELADA')
    
    if filtro4 == '1':        
        residencias = residencias.filter(dependencia__isnull = True)
        filtros_list.append('Sin organizacion o empresa')    
    elif filtro4 == '2':        
        residencias = residencias.filter(dependencia__isnull = False)
        filtros_list.append('Con organizacion o empresa')    
    elif filtro4 != '0':
        dependencia = Dependencia.objects.get(id = filtro4)
        residencias = residencias.filter(dependencia = dependencia)
        filtros_list.append(f'Organizacion o empresa: {dependencia.d_nombre}') 
        
    if periodo_inicio_de_obj:
        if periodo_inicio_hasta_obj:
            residencias = residencias.filter(periodoInicio__range=(periodo_inicio_de_obj, periodo_inicio_hasta_obj))                        
            date_time_str1 = periodo_inicio_de_obj.strftime("%d - %b - %Y")
            date_time_str2 = periodo_inicio_hasta_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Periodo inicio a partir de: {date_time_str1} hasta {date_time_str2}')            
        else:
            residencias = residencias.filter(periodoInicio__gte=periodo_inicio_de_obj)        
            date_time_str = periodo_inicio_de_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Periodo inicio a partir de: {date_time_str}')        
    
    if filtro5 == '1' and filtro6 == '1':
        filtros_list.append('Sin periodo de inicio')  
        residencias = residencias.filter(periodoInicio__isnull = True)      
    elif filtro5 == '2' and filtro6 == '2':
        residencias = residencias.filter(periodoInicio__isnull = False)      
        filtros_list.append('Con periodo de inicio')        
        
    if periodo_inicio_hasta_obj:
        if not periodo_inicio_de_obj:
            residencias = residencias.filter(periodoInicio__lte=periodo_inicio_hasta_obj)
            date_time_str = periodo_inicio_hasta_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Periodo inicio hasta: {date_time_str}')        
                    
    if periodo_fin_de_obj:
        if periodo_fin_hasta_obj:
            residencias = residencias.filter(periodoFin__range=(periodo_fin_de_obj, periodo_fin_hasta_obj))                        
            date_time_str1 = periodo_fin_de_obj.strftime("%d - %b - %Y")
            date_time_str2 = periodo_fin_hasta_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Periodo fin a partir de: {date_time_str1} hasta {date_time_str2}')            
        else:
            residencias = residencias.filter(periodoFin__gte=periodo_fin_de_obj)        
            date_time_str = periodo_fin_de_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Periodo fin a partir de: {date_time_str}')        
    
    if filtro7 == '1' and filtro8 == '1':
        filtros_list.append('Sin periodo de fin')        
        residencias = residencias.filter(periodoFin__isnull = True)      
    elif filtro7 == '2' and filtro8 == '2':
        filtros_list.append('Con periodo de fin')        
        residencias = residencias.filter(periodoFin__isnull = False)      
        
    if periodo_fin_hasta_obj:
        if not periodo_fin_de_obj:
            residencias = residencias.filter(periodoFin__lte=periodo_fin_hasta_obj)
            date_time_str = periodo_fin_hasta_obj.strftime("%d - %b - %Y")
            filtros_list.append(f'Periodo fin hasta: {date_time_str}')        
            
        
    return residencias, filtros_list

def filtrar_estudiantes_aut(all_estudiantes, filtros):
    estudiantes = all_estudiantes
    
    filtro1 = filtros[0]
    filtro2 = filtros[1]
    
    if filtro1 == 1:
        estudiantes = estudiantes.filter(is_registrado = True)
    elif filtro1 == 2:
        estudiantes = estudiantes.filter(is_registrado = False)
    
    if filtro2 != '0':                
        estudiantes = estudiantes.filter(num_control__startswith = filtro2)
    
    return estudiantes