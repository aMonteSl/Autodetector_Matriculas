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

Antes de comenzar, puedes elegir tu método preferido para la instalación:

- **Opción 1: Instrucciones Escritas:** Sigue los pasos detallados a continuación.
- **Opción 2: Video Tutorial:** [Haz clic aquí para ver el video tutorial de instalación](enlace-al-video).

Si prefieres instrucciones escritas, sigue los pasos a continuación:

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

![](Images/tesseract_)

[^1]: en caso de no tener instalado pip --> `sudo apt install python3-pip`.


> [!CAUTION]
> Esta instalación no es trivial y pueden surgir problemas en el camino. Si tienes alguno, por favor contacta conmigo por correo o teléfono: 
> - c.nebril.2020@alumnos.urjc.es
> - 654631207


## 3. Metodología 🛠️

Vamos a pasar al 

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


