from datetime import date
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .models import *


class EstudianteForm(ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
        exclude = ['domicilio', 'user', 'expediente', 'anteproyecto', 'residencia', 'id', 'estudiante_aut', 'carrera']
        labels = {
            'nombre': 'Nombre(s)',
            'apellidoP': 'Apellido Paterno',
            'apellidoM': 'Apellido Materno',
            'numCelular': 'Numero de celular',
            'numControl': 'Numero de control',                  
        }
    
    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            if myField == 'semestre':                
                self.fields[myField].widget.attrs['class'] = 'block w-12 mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                
            else:
                self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        labels = {            
            'email': 'Correo institucional',
            'password1': 'Password'            
        }
        
    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            domain = data.split('@')[1]
            domain_list = ["itoaxaca.edu.mx", "oaxaca.tecnm.mx",]
            if domain not in domain_list:
                raise forms.ValidationError("Solo se acepta el correo institucional")
            elif User.objects.filter(email=data).exists():
                raise forms.ValidationError("Existe otro estudiante con este correo electrónico.")
        else:
            raise forms.ValidationError("El correo institucional no puede estar vacio")
                    
            
        return data
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for myField in self.fields:                        
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class CreateUserFormEmail(ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {            
            'email': 'Correo institucional',            
        }
        
    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            domain = data.split('@')[1]
            domain_list = ["itoaxaca.edu.mx", "oaxaca.tecnm.mx",]
            if domain not in domain_list:
                raise forms.ValidationError("Solo se acepta el correo institucional")
        else:
            data = None
        return data
        
    def __init__(self, *args, **kwargs):
        super(CreateUserFormEmail, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class CreateUserFormDocente(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        labels = {            
            'email': 'Correo institucional',            
        }
        
    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            domain = data.split('@')[1]
            domain_list = ["itoaxaca.edu.mx", "oaxaca.tecnm.mx",]
            if domain not in domain_list:
                raise forms.ValidationError("Solo se acepta el correo institucional")
        else:
            data = None
        return data
        
    def __init__(self, *args, **kwargs):
        super(CreateUserFormDocente, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
        labels = {
            'old_password': 'Contraseña actual',
            'new_password1': 'Contraseña nueva',
            'new_password2': 'Confirmacion contraseña'            
        }
        
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class ResetPasswordForm(PasswordResetForm):
    class Meta:
        model = User
        fields = '__all__'        
        
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            self.fields[myField].label = ''

class DomicilioForm(ModelForm):
    class Meta:
        model = Domicilio
        fields = '__all__'
        exclude = ['id']
        labels = {'codigoPostal': 'Codigo Postal'}

    def __init__(self, *args, **kwargs):
        super(DomicilioForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            
class DomicilioViewForm(ModelForm):
    class Meta:
        model = Domicilio
        fields = '__all__'
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        super(DomicilioViewForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'        
            self.fields[myField].widget.attrs['disabled'] = True

class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = '__all__'
        exclude = ['reporteParcial1', 'reporteParcial2', 'reporteFinal', 'estatus', 'id']
        labels = {
            'anteproyecto': 'Anteproyecto autorizado',
            'solicitudResidencia': 'Solicitud Residencia',
            'cartaPresentacion': 'Carta Presentacion',
            'cartaCompromiso': 'Carta Compromiso',
            'cartaAceptacion': 'Carta Aceptacion',
            'cartaLiberacion': 'Carta de Liberacion',            
            'manualUsuario': 'Manual de Usuario',            
            'manualTecnico': 'Manual Tecnico',                        
        }

    def __init__(self, *args, **kwargs):
        super(ExpedienteForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            self.fields[myField].widget.attrs['accept'] = '.pdf'  
            
class ExpedienteViewForm(ModelForm):
    class Meta:
        model = Expediente
        fields = '__all__'
        exclude = ['reporteParcial1', 'reporteParcial2', 'reporteFinal', 'estatus', 'id']
        labels = {
            'anteproyecto': 'Anteproyecto autorizado',
            'solicitudResidencia': 'Solicitud Residencia',
            'cartaPresentacion': 'Carta Presentacion',
            'cartaCompromiso': 'Carta Compromiso',
            'cartaAceptacion': 'Carta Aceptacion',
            'cartaLiberacion': 'Carta de Liberacion',            
            'manualUsuario': 'Manual de Usuario',            
            'manualTecnico': 'Manual Tecnico',                   
        }

    def __init__(self, *args, **kwargs):
        super(ExpedienteViewForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            
            self.fields[myField].widget.attrs['disabled'] = True

class Reporte1Form(ModelForm):
    class Meta:
        model = ReporteParcial1
        fields = '__all__'
        exclude = ['r1_fechaEntrega', 'id']
        labels = {
            'r1_hojaRevisores': 'Hoja Revisores',
            'r1_formatoEvaluacion': 'Formato Evaluacion',
        }
        
    def __init__(self, *args, **kwargs):
        super(Reporte1Form, self).__init__(*args, **kwargs)        
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'        
            self.fields[myField].widget.attrs['accept'] = '.pdf'  

class Reporte2Form(ModelForm):
    class Meta:
        model = ReporteParcial2
        fields = '__all__'
        exclude = ['r2_fechaEntrega', 'id']
        labels = {
            'r2_hojaRevisores': 'Hoja Revisores',
            'r2_formatoEvaluacion': 'Formato Evaluacion',
        }

    def __init__(self, *args, **kwargs):
        super(Reporte2Form, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                    
            self.fields[myField].widget.attrs['accept'] = '.pdf'  

class ReporteFinalForm(ModelForm):
    class Meta:
        model = ReporteFinal
        fields = '__all__'
        exclude = ['rf_fechaEntrega', 'calificacion', 'id']
        labels = {
            'rf_hojaRevisores': 'Hoja Revisores',
            'rf_formatoEvaluacion': 'Formato Evaluacion',
        }

    def __init__(self, *args, **kwargs):
        super(ReporteFinalForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                    
            self.fields[myField].widget.attrs['accept'] = '.pdf'  

class DocenteForm(ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'
        exclude = ['user', 'perfilAcademico', 'id']
        labels = {
            'curp': 'CURP',
            'rfc': 'RFC',
            'nombre': 'Nombre(s)',
            'apellidoP': 'Apellido Paterno',
            'apellidoM': 'Apellido Materno',
            'numCelular': 'Numero de celular',
        }

    def __init__(self, *args, **kwargs):
        super(DocenteForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            
class AnteproyectoEstForm(ModelForm):
    class Meta:
        today = date.today()
        YEARSI= [x for x in range(today.year,today.year+1)]
        YEARSF= [x for x in range(today.year,today.year+3)]
        model = Anteproyecto
        fields = '__all__'
        exclude = ['revisor1', 'revisor2', 'dependencia', 'asesorExterno', 'observacion', 'estatusR1', 'estatusR2', 'id', 'fechaEntrega', 'estatus', 'codigoUnion']   
        labels = {
            'a_nombre': 'Nombre del Anteproyecto',
            'tipoProyecto': 'Tipo de Proyecto',
            'fechaEntrega': 'Fecha de entrega',
            'numIntegrantes': 'Numero de integrantes',            
            'anteproyectoDoc': 'Documento del anteproyecto'
        }
        widgets = {
            'periodoInicio': forms.SelectDateWidget(years=YEARSI),
            #'periodoInicio': forms.DateField(widget=forms.SelectDateWidget(years=YEARS)),
            'periodoFin': forms.SelectDateWidget(years=YEARSF),
        }
                

    def __init__(self, *args, **kwargs):
        super(AnteproyectoEstForm, self).__init__(*args, **kwargs)        
        for myField in self.fields:            
            if myField == 'periodoInicio' or myField == 'periodoFin':                
                self.fields[myField].widget.attrs['class'] = 'ml-4 mt-2 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                
            elif myField == 'anteproyectoDoc':
                self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
                self.fields[myField].widget.attrs['accept'] = '.pdf'  
            else :
                self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            
class AnteproyectoViewForm(ModelForm):
    class Meta:
        model = Anteproyecto
        fields = '__all__'     
        exclude = ['revisor1', 'revisor2', 'dependencia', 'asesorExterno', 'anteproyectoDoc', 'observacion', 'estatus', 'estatusR1', 'estatusR2', 'id', 'codigoUnion']   
        labels = {
            'a_nombre': 'Nombre del Anteproyecto',
            'tipoProyecto': 'Tipo de Proyecto',
            'fechaEntrega': 'Fecha de entrega',
            'numIntegrantes': 'Numero de integrantes',            
            'periodoInicio': 'Fecha inicio',            
            'periodoFin': 'Fecha Fin',            
        }        

    def __init__(self, *args, **kwargs):
        super(AnteproyectoViewForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            if myField == 'numIntegrantes':
                self.fields[myField].widget.attrs['class'] = 'block w-12 mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            
            else:
                self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            
            self.fields[myField].widget.attrs['disabled'] = True

class AnteproyectoForm(ModelForm):
    class Meta:
        model = Anteproyecto
        fields = '__all__'
        exclude = ['asesorInterno', 'revisor','dependencia', 'asesorExterno', 'anteproyectoDoc', 'observacion', 'estatusR1', 'estatusR2', 'id', 'fechaEntrega']   
        labels = {
            'a_nombre': 'Nombre del anteproyecto',
        }        

    def __init__(self, *args, **kwargs):
        super(AnteproyectoForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                        

class AnteproyectoEditForm(ModelForm):
    class Meta:        
        model = Anteproyecto
        fields = '__all__'
        exclude = ['revisor1', 'revisor2', 'dependencia', 'asesorExterno', 'observacion', 'estatusR1', 'estatusR2', 'id', 'fechaEntrega', 'estatus', 'codigoUnion', 'anteproyectoDoc']   
        labels = {
            'a_nombre': 'Nombre del Anteproyecto',
            'tipoProyecto': 'Tipo de Proyecto',
            'fechaEntrega': 'Fecha de entrega',
            'numIntegrantes': 'Numero de integrantes',                        
        }                        

    def __init__(self, *args, **kwargs):
        super(AnteproyectoEditForm, self).__init__(*args, **kwargs)        
        for myField in self.fields:                                    
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            
class AnteproyectoDocForm(ModelForm):
    class Meta:
        model = Anteproyecto
        fields = ['anteproyectoDoc']        
        labels = {
            'anteproyectoDoc': 'Anteproyecto',
        }        

    def __init__(self, *args, **kwargs):
        super(AnteproyectoDocForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                                    
            self.fields[myField].widget.attrs['accept'] = '.pdf'  

class ResidenciaForm(ModelForm):
    class Meta:
        model = Residencia
        fields = '__all__'
        exclude = ['dependencia', 'asesorExterno', 'r_asesorInterno', 'r_revisor', 'id']
        labels = {
            'nombre': 'Nombre del proyecto de Residencia',
            'tipoProyecto': 'Tipo de Proyecto',
            'fechaEntrega': 'Fecha de entrega',
            'numIntegrantes': 'Numero de integrantes',            
            'periodoInicio': 'Fecha inicio',            
            'periodoFin': 'Fecha Fin',            
        }   
    
    def __init__(self, *args, **kwargs):
        super(ResidenciaForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                                         

class ResidenciaDateForm(ModelForm):
    class Meta:
        model = Residencia
        fields = ['periodoInicio', 'periodoFin']        
        labels = {                    
            'periodoInicio': 'Fecha inicio',            
            'periodoFin': 'Fecha Fin',            
        }   
    
    def __init__(self, *args, **kwargs):
        super(ResidenciaDateForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            #self.fields[myField].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  
            self.fields[myField].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  
            #self.fields[myField].widget = extras.SelectDateWidget
            print(myField)
            if myField == 'periodoInicio':
                self.fields[myField].widget.attrs['placeholder'] = 'Periodo de Inicio'
                self.fields[myField].widget.attrs['id'] = 'id_periodoI'                
            else:
                self.fields[myField].widget.attrs['placeholder'] = 'Periodo de Fin'
                self.fields[myField].widget.attrs['id'] = 'id_periodoF'

class ResidenciaViewForm(ModelForm):
    class Meta:
        model = Residencia
        fields = '__all__'
        exclude = ['dependencia', 'asesorExterno', 'r_asesorInterno', 'r_revisor', 'id', 'estatus']
        labels = {
            'nombre': 'Nombre del proyecto de Residencia',
            'tipoProyecto': 'Tipo de Proyecto',
            'fechaEntrega': 'Fecha de entrega',
            'numIntegrantes': 'Numero de integrantes',            
            'periodoInicio': 'Fecha inicio',            
            'periodoFin': 'Fecha Fin',            
        }   
    
    def __init__(self, *args, **kwargs):
        super(ResidenciaViewForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            if myField == 'numIntegrantes':
                self.fields[myField].widget.attrs['class'] = 'block w-12 mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            
            else:
                self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                             
            self.fields[myField].widget.attrs['disabled'] = True
                    
class DependenciaForm(ModelForm):
    class Meta:
        model = Dependencia
        fields = '__all__'
        exclude = ['domicilio', 'titular', 'id']
        labels = {
            'd_nombre': 'Nombre de la Organizacion o Empresa',
            'rfc': 'RFC (Elimina espacios y guiones)',
            'numCelular': 'Numero de Celular',
            'correoElectronico': 'Correo Electronico',            
        }

    def __init__(self, *args, **kwargs):
        super(DependenciaForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            if myField == 'mision':
                self.fields[myField].widget = forms.Textarea()
                self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
                                            
class DependenciaViewForm(ModelForm):
    class Meta:
        model = Dependencia
        fields = '__all__'
        exclude = ['domicilio', 'titular', 'id']
        labels = {
            'd_nombre': 'Nombre',
            'rfc': 'RFC',
            'numCelular': 'Numero de Celular',
            'correoElectronico': 'Correo Electronico',            
        }

    def __init__(self, *args, **kwargs):
        super(DependenciaViewForm, self).__init__(*args, **kwargs)
        for myField in self.fields:            
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            self.fields[myField].widget.attrs['disabled'] = True            
        
class TitularForm(ModelForm):
    class Meta:
        model = TitularDependencia
        fields = '__all__'
        exclude = ['id']
        labels = {
            't_nombre': 'Nombre(s)',
            't_apellidoP': 'Apellido Paterno',
            't_apellidoM': 'Apellido Materno',
            't_puesto': 'Puesto'
        }
    
    def __init__(self, *args, **kwargs):
        super(TitularForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class TitularViewForm(ModelForm):
    class Meta:
        model = TitularDependencia
        fields = '__all__'
        exclude = ['id']
        labels = {
            't_nombre': 'Nombre(s)',
            't_apellidoP': 'Apellido Paterno',
            't_apellidoM': 'Apellido Materno',
            't_puesto': 'Puesto'
        }
    
    def __init__(self, *args, **kwargs):
        super(TitularViewForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            self.fields[myField].widget.attrs['disabled'] = True
            
class AsesorEForm(ModelForm):
    class Meta:
        model = AsesorExterno
        fields = '__all__'   
        exclude = ['dependencia', 'id']
        labels = {
            'nombre': 'Nombre(s)',
            'apellidoP': 'Apellido Paterno',
            'apellidoM': 'Apellido Materno',
        }
    
    def __init__(self, *args, **kwargs):
        super(AsesorEForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            
class AsesorEViewForm(ModelForm):
    class Meta:
        model = AsesorExterno
        fields = '__all__'   
        labels = {
            'nombre': 'Nombre(s)',
            'apellidoP': 'Apellido Paterno',
            'apellidoM': 'Apellido Materno',
        }
    
    def __init__(self, *args, **kwargs):
        super(AsesorEViewForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            
            self.fields[myField].widget.attrs['disabled'] = True

class ObservacionDocenteForm(ModelForm):
    class Meta:
        model = ObservacionDocente
        fields = ['observacionD']
        labels = {
            'observacionD': 'Descripcion de la observacion'
        }
    
    def __init__(self, *args, **kwargs):
        super(ObservacionDocenteForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            
