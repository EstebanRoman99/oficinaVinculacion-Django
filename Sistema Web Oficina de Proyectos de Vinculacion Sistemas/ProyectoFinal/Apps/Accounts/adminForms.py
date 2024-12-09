from datetime import date
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import *
from django.core.validators import FileExtensionValidator

class AnteproyectoEstadoForm(ModelForm):
    class Meta:
        model = Anteproyecto
        fields = ['estatus']
        labels = {
            'estatus': ''
        }
    
    def __init__(self, *args, **kwargs):
        super(AnteproyectoEstadoForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class AnteproyectoEstadoFormR1(ModelForm):
    class Meta:
        model = Anteproyecto
        fields = ['estatusR1']
        labels = {
            'estatusR1': ''
        }
    
    def __init__(self, *args, **kwargs):
        super(AnteproyectoEstadoFormR1, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'

class AnteproyectoEstadoFormR2(ModelForm):
    class Meta:
        model = Anteproyecto
        fields = ['estatusR2']
        labels = {
            'estatusR2': ''
        }
    
    def __init__(self, *args, **kwargs):
        super(AnteproyectoEstadoFormR2, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
           
class ExpedienteEstadoForm(ModelForm):
    class Meta:
        model = Expediente
        fields = ['estatus']
        labels = {
            'estatus': ''
        }
    
    def __init__(self, *args, **kwargs):
        super(ExpedienteEstadoForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'        
            
class ResidenciaEstadoForm(ModelForm):
    class Meta:
        model = Residencia
        fields = ['estatus']
        labels = {
            'estatus': ''
        }
    
    def __init__(self, *args, **kwargs):
        super(ResidenciaEstadoForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            

ENTIDADES = (('ESTUDIANTES', 'ESTUDIANTES'), ('DOCENTES', 'DOCENTES'), ('TODOS', 'TODOS'))
class AvisosForm(ModelForm):    
    class Meta:
        model = Avisos
        fields = '__all__'
        exclude = ['id' ,'estudiante', 'docente']
        labels = {
            'entidad': 'Dirigido a',
            'tiempoVida': 'Tiempo de duracion del aviso (dias)'
            }
    
    def __init__(self, *args, **kwargs):
        super(AvisosForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'                        
            if myField == 'entidad':
                self.fields[myField].choices = ENTIDADES
                print(self.fields[myField].choices)

class MateriaForm(ModelForm):
    class Meta:
        model = Materia
        fields = '__all__'
        exclude = ['id']        
    
    def __init__(self, *args, **kwargs):
        super(MateriaForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'            
            
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': '.csv'}), validators=[FileExtensionValidator(['csv'])])
    
    def __init__(self, *args, **kwargs):
        super(CSVUploadForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].label = ''
            self.fields[myField].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
    
                                        