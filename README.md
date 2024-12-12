# RepositorioSistemaWebOficinadeVinculacion
Repositorio del sistema web para la gestión de información de la Oficina de Proyectos de Vinculación en el Instituto Tecnológico de Oaxaca.

## Descripción
Sistema desarrollado para facilitar la administración y seguimiento de proyectos de vinculación. El sistema incluye un modelo de inteligencia artificial para análisis y predicciones relacionadas con los proyectos, con una interfaz moderna y responsiva diseñada con Tailwind CSS.

## Tecnologías
- **Framework Backend:** Django
- **Framework Frontend:** Tailwind CSS
- **Base de Datos:** PostgreSQL
- **Inteligencia Artificial:** Python (librerías utilizadas como TensorFlow o PyTorch, si corresponde)

## Instalación
Sigue estos pasos para instalar y ejecutar el sistema:

# Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar las dependencias
pip install -r requirements.txt

# Aplicar las migraciones
python manage.py migrate

# Ejecutar el servidor
python manage.py runserver
