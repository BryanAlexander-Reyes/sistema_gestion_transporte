import os
from decouple import config

# LEER EL PUERTO
port =config('API_PORT')

# ejecutar el servidor de django

os.system(f'python manage.py runserver {port}')