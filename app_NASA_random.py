import requests
from datetime import datetime, timedelta
import random
from pprint import PrettyPrinter
import streamlit as st
import os



# Asumiendo que ya tienes definida tu variable api_key
api_key = 'XRBEsdQBfc8lSCkfnW1mWZdBgx0f3M5LNEsntUGM'
pp = PrettyPrinter()

def delete_jpg_files():
    # Obtener la lista de todos los archivos en el directorio actual
    files_in_directory = os.listdir()
    # Filtrar la lista para incluir sólo archivos que terminen en '.jpg'
    jpg_files = [file for file in files_in_directory if file.endswith('.jpg')]
    
    # Contador de archivos eliminados
    deleted_files_count = 0

    # Recorrer la lista de archivos jpg y eliminarlos
    for file in jpg_files:
        try:
            os.remove(file)
            print(f'Archivo eliminado: {file}')
            deleted_files_count += 1
        except Exception as e:
            print(f'Error al eliminar el archivo {file}: {e}')
    
    # Informar al usuario el número de archivos eliminados
    if deleted_files_count == 0:
        print("No se encontraron archivos .jpg para eliminar.")
    else:
        print(f"Total de archivos .jpg eliminados: {deleted_files_count}")

def fetchAPOD(random_date=False):
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    if random_date:
        start_date = datetime(1995, 6, 16)  # Fecha de inicio del servicio APOD
        end_date = datetime.now()  # Fecha actual
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        date = start_date + timedelta(days=random_number_of_days)
        date_str = date.strftime('%Y-%m-%d')
    else:
        date_str = '2020-01-22'  # Usar una fecha fija si random_date no es True

    params = {
        'api_key': api_key,
        'date': date_str,
        'hd': 'True'
    }
    response = requests.get(URL_APOD, params=params).json()
    #pp.pprint(response)
    
    # Procesar la respuesta como antes
    if 'hdurl' in response:
        image_url = response['hdurl']
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            filename = image_url.split("/")[-1]
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print("Título de la imagen: " + response.get('title', 'Sin título'))
            print(f'La imagen ha sido guardada con éxito como: {filename}')
        else:
            print('No se pudo descargar la imagen')
    else:
        print('No se encontró una URL de imagen en la respuesta')
    return response, filename

# Para obtener una imagen de una fecha específica (2020-01-22)
# fetchAPOD()

# Para obtener una imagen aleatoria


st.header("App de imágenes de la NASA")
st.text("Oprime el botón para ver la magia")
boton = st.button("Ver la magia")

print(boton)

if boton:
    respuesta, archivo=fetchAPOD(random_date=True)
    st.image(str(archivo), caption=respuesta['title'])
    st.text("Datos de la imagen")
    st.json(respuesta)
    delete_jpg_files()
    
    