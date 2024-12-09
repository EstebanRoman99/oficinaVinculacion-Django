from django.core.exceptions import ValidationError

# Validator
def validate_nonzero(value):
    if value == 0:
        raise ValidationError("El tiempo debe ser mayor a 0")
    
def validate_len_num_control(value):
    len_num_control = len(value)
    if len_num_control < 8:
        raise ValidationError("Número de control no valido")

# Ponerle este validator a cada FileField
def validate_file_size(file):
    # La unidad esta en Bytes
    max_upload_size = 5242880  # 5MB
    if file.size > max_upload_size:
        raise ValidationError("El tamaño del archivo es mayor que el límite permitido")