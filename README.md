# DETECTOR DE MATRÍCULAS 
  Este programa identifica el texto asociado a la matrícula de un vehículo presente en una imagen.

# FUNCIONAMIENTO
  Este programa emplea avanzadas técnicas de procesamiento de imágenes para la detección de matrículas en una imagen. El proceso se divide en dos fases fundamentales:

  ## 1. Segmentación de Matrículas:
  Mediante el empleo de técnicas de procesamiento de imágenes, podremos reconocer la matrícula de un vehículo en una imagen. Posteriormente, almacenaremos dicha matrícula como otra imagen independiente, la cual será utilizada en la siguiente fase.
    
  ## 2. Reconocimento de Texto:
  En esta etapa, empleamos una biblioteca externa denominada PYTESSERACT para extraer el texto de la matrícula. Esta biblioteca incluye un modelo preentrenado específicamente para esta tarea. Más adelante, proporcionaremos instrucciones detalladas sobre la instalación de la biblioteca y explicaremos cómo realiza la detección del texto.

  ## Extra:
  Además, en el proceso de ejecución del programa crearemos distintos .txt donde podremos ir viendo lo que ocurre internamente en el programa, a continuación un ejemplo de cada .txt:
  
  ### 1. User_inputs: Este fichero contendra la información de que imagenes a seleccionado el usuario, el nombre del fichero imagen que ha seleccionado y el directorio donde se encuentra la imagen, ejemplo:
  User choice: 1, Selected image: 1_Coche.jpg. Path: C:\Users\adrian\Escritorio\AutoMatriculas\DetectedPlates\plate1.jpg
  User choice: 8, Selected image: 8_Coche.jpg. Path: C:\Users\adrian\Escritorio\AutoMatriculas\DetectedPlates\plate8.jpg
  ### 2. License_plates_text: En este fichero guardaremos la información respecto el nombre de la imagen que contiene la matricula (es decir la imagen generada en la primera fase) y el texto que se ha detectado en dicha imagen, ejemplo:
  Image Path: plate1.jpg, Plate Text: B2228HM
  Image Path: plate8.jpg, Plate Text: 0007LLL
  ### 3. License_plates_reader: En este fichero simplemente se guardan errores que ocurran en la segunda fase, como por ejemplo que no se haya podido detectar texto en la imagen o errores similaresm, ejemplo:
  ERROR:root:Error while processing images: 'NoneType' object has no attribute 'group'
      



