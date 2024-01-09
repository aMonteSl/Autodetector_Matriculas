# Proyecto Final - Asignatura TIM 🚀

## 1. Introducción y Objetivo ℹ️

Este repositorio contiene el proyecto final desarrollado para la asignatura de  (TIM) en la Universidad Rey Juan Carlos. El objetivo principal del proyecto es la **segmentación y reconocimiento de matrículas**, es decir:

* Obtener una imagen independiente solamente con la matricula.
* Generar un texto equivalente a los carácteres de la matricula.

Para la resolución del problema se han puesto en práctica los conceptos vistos en el tema 2 (tratamiento de imágenes), y la implementación de un modelo entrenado (esencialmente un decisor) que nos ayuda a identificar los carácteres en la matricula. 

## 2. Demo e Instalación

Antes de indagar en el proyecto a fondo, os presentamos una **demonstración** del programa y una serie de instrucciones por si quereis **probar** la implementación vosotros mismos.

- [**Haz click aquí para ver el video demonstración**](enlace-al-video)

### ¡Pruebalo tu mismo! (Ubuntu)

1. **Paso 1:** Clona el repositorio en tu máquina local.

    ```bash
    git clone https://github.com/aMonteSl/Autodetector_Matriculas.git
    ```

2. **Paso 2:** Navega al directorio del proyecto.

    ```bash
    cd Autodetector_Matriculas
    ```

3. **Paso 3:** Instala las dependencias[^1].

    ```bash
    pip install -r requirements.txt 
    ```

4. **Paso 4:** Instalamos el modelo entrenado y mas dependencias.

    ```bash
    sudo apt install tesseract-ocr
    sudo apt install libtesseract-dev
    ```

5. **Paso 5:** Copiamos la salida de este comando.

    ```bash
    which tesseract
    ```

6. **Paso 6:** Configuramos el programa.

- Abrimos en nuestro editor favorito el programa `character_decider.py`. Pegamos en la línea 17 la salida del comando anterior. En mi caso quedaría algo así:

![](Images/tesseract_path.png)

[^1]: en caso de no tener instalado pip --> `sudo apt install python3-pip`.

### ¡Pruebalo tu mismo! (Windows)

Escribe aqui los pasos adrian.

> [!WARNING]
> Esta instalación no es trivial y pueden surgir problemas en el camino. Si tienes alguno, por favor contacta con nosotros por correo o teléfono: 
> - c.nebril.2020@alumnos.urjc.es
> - 654631207


## 3. Metodología 🛠️

Este programa emplea avanzadas técnicas de procesamiento de imágenes para la detección de matrículas en una imagen. El proceso se divide en dos fases fundamentales:

  ### 1. Segmentación de Matrículas:
  Mediante el empleo de técnicas de procesamiento de imágenes, podremos reconocer la matrícula de un vehículo en una imagen. Posteriormente, almacenaremos dicha matrícula como otra imagen independiente, la cual será utilizada en la siguiente fase.
    
  ### 2. Reconocimento de Texto:
  En esta etapa, empleamos una biblioteca externa denominada PYTESSERACT para extraer el texto de la matrícula. Esta biblioteca incluye un modelo preentrenado específicamente para esta tarea. Más adelante, proporcionaremos instrucciones detalladas sobre la instalación de la biblioteca y explicaremos cómo realiza la detección del texto.

  ### Extra:
  Además, en el proceso de ejecución del programa crearemos distintos .txt donde podremos ir viendo lo que ocurre internamente en el programa, a continuación un ejemplo de cada .txt:

  #### 1. User_inputs: 
  Este fichero contendra la información de que imagenes a seleccionado el usuario, el nombre del fichero imagen que ha seleccionado y el directorio donde se encuentra la imagen, ejemplo:

  User choice: 1, Selected image: 1_Coche.jpg. Path: C:\Users\adrian\Escritorio\AutoMatriculas\DetectedPlates\plate1.jpg

  User choice: 8, Selected image: 8_Coche.jpg. Path: C:\Users\adrian\Escritorio\AutoMatriculas\DetectedPlates\plate8.jpg
  #### 2. License_plates_text: 
  En este fichero guardaremos la información respecto el nombre de la imagen que contiene la matricula (es decir la imagen generada en la primera fase) y el texto que se ha detectado en dicha imagen, ejemplo:

  Image Path: plate1.jpg, Plate Text: B2228HM

  Image Path: plate8.jpg, Plate Text: 0007LLL
  #### 3. License_plates_reader: 
  En este fichero simplemente se guardan errores que ocurran en la segunda fase, como por ejemplo que no se haya podido detectar texto en la imagen o errores similaresm, ejemplo:

  ERROR:root:Error while processing images: 'NoneType' object has no attribute 'group'
      



## 4. Resultados 📊

Los resultados obtenidos durante la implementación incluyen [descripción de los resultados más relevantes o hallazgos importantes].

## 5. Discusión 💬

Se discuten los resultados obtenidos en relación con [estándares, trabajos previos, etc.]. Además, se analizan posibles limitaciones, áreas de mejora y aspectos relevantes.

## 6. Conclusión 🎯

En conclusión, [resumen de las conclusiones principales]. Se destaca la importancia de los hallazgos y se mencionan posibles direcciones futuras para la investigación o aplicaciones.

## 7. Referencias 📜

Se proporciona un listado de las fuentes bibliográficas, recursos y documentos consultados durante el desarrollo del proyecto.

---

¡Gracias por visitar nuestro repositorio! Esperamos que encuentres este proyecto interesante y útil. 👩‍💻👨‍💻


