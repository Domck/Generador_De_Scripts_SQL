
# Generador de Scripts SQL desde Excel

Este programa automatiza la creación de scripts SQL a partir de archivos Excel, permitiendo la generación de tablas, `INSERT` y `DELETE` con compatibilidad total en el manejo de tipos de datos. La aplicación está diseñada para optimizar procesos, reducir errores y facilitar la integración de datos en bases de datos relacionales.

## **Características**

- Genera scripts SQL (`CREATE TABLE`, `INSERT INTO`, y `DELETE`) a partir de un archivo Excel.
- Crea tablas automáticamente basadas en la cantidad de hojas presentes en el archivo Excel.
- Manejo dinámico de tipos de datos para respetar el formato del contenido en las celdas.
- Genera un archivo con los scripts SQL en el escritorio del usuario.
- Funcionalidad para subir y gestionar archivos de Excel para su procesamiento.
- **API REST** integrada para automatizar el flujo de trabajo (opcional, según implementación).

## **Cómo funciona**

1. El programa recibe un archivo Excel como entrada.
2. Procesa cada hoja del Excel, generando automáticamente los scripts SQL correspondientes:
   - **CREATE TABLE**: Basado en los nombres y tipos de datos encontrados.
   - **INSERT INTO**: Para insertar los datos contenidos en cada hoja.
   - **DELETE**: Scripts para eliminar los datos en caso necesario.
3. El resultado es un archivo con los scripts SQL, que se guarda automáticamente en el escritorio del usuario.

## **Ventajas**

- **Automatización**: Reduce significativamente el tiempo necesario para generar scripts SQL.
- **Precisión**: Minimiza errores en la manipulación de datos gracias al manejo dinámico de tipos de caracteres.
- **Flexibilidad**: Adaptable a diferentes estructuras de datos contenidas en el archivo Excel.
- **Optimización del tiempo**: Ideal para equipos que requieren integrar datos de manera recurrente.

## **Requisitos**

- Python 3.8 o superior.
- Librerías necesarias: 
  - `pandas` (procesamiento de Excel).
  - `openpyxl` (lectura/escritura de Excel).
  
  Puedes instalar las dependencias ejecutando:
  ```bash
  pip install -r requirements.txt
python main.py
![image](https://github.com/user-attachments/assets/6418d0f0-8f34-4a86-8559-aa7ccc4ff45d)

# python -m venv env
# .\env\Scripts\Activate.ps1
# pip install pandas
# pip install openpyxl
# pip install flask 
# deactivate
