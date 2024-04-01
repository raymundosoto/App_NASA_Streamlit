import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter
pp = PrettyPrinter()


api_key = 'XRBEsdQBfc8lSCkfnW1mWZdBgx0f3M5LNEsntUGM'

# def fetchEPICImage():
#   YEAR = '2015'
#   MONTH = '10'
#   DAY = '31'
#   IMAGE_ID = 'epic_1b_20151031074844'
#   URL_EPIC = "https://epic.gsfc.nasa.gov/archive/natural/"
#   URL_EPIC = URL_EPIC + YEAR +'/' + MONTH + '/'+DAY
#   URL_EPIC = URL_EPIC + '/png'
#   URL_EPIC = URL_EPIC + '/' + IMAGE_ID + '.png' 
#   print(URL_EPIC)
#   urlretrieve(URL_EPIC,IMAGE_ID+'.png')
  



def fetchAPOD():
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    date = '2020-01-22'
    params = {
        'api_key': api_key,
        'date': date,
        'hd': 'True'
    }
    response = requests.get(URL_APOD, params=params).json()
    #pp.pprint(response)  #Imprimir respuestas
    
    # Verifica si la respuesta incluye una URL de imagen
    if 'hdurl' in response:
        image_url = response['hdurl']
        
        # Hacemos la petición GET a la URL de la imagen
        img_response = requests.get(image_url)
        
        # Verificamos que la petición fue exitosa
        if img_response.status_code == 200:
            # Extraemos el nombre del archivo de la URL
            filename = image_url.split("/")[-1]
            
            # Abrimos un nuevo archivo en modo binario para escribir el contenido de la imagen
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print("Nombre de la imagen descargada"+ " " + response['title'])
            print(f'La imagen ha sido guardada con éxito como: {filename}')
        else:
            print('No se pudo descargar la imagen')
    else:
        print('No se encontró una URL de imagen en la respuesta')

# Ejecuta la función
fetchAPOD()
#fetchEPICImage()