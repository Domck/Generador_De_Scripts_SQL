from flask import Flask, request, jsonify, render_template, send_file
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__, template_folder='.')

def obtener_ruta_escritorio():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def crear_carpeta_configs():
    ruta_escritorio = obtener_ruta_escritorio()
    carpeta_configs = os.path.join(ruta_escritorio, "Configs")
    if not os.path.exists(carpeta_configs):
        os.makedirs(carpeta_configs)
    return carpeta_configs

@app.route('/')
def index():
    crear_carpeta_configs()
    return render_template('index.html')

@app.route('/list-files', methods=['GET'])
def list_files():
    carpeta_configs = crear_carpeta_configs()
    try:
        files = [f for f in os.listdir(carpeta_configs) if f.endswith('.xlsx')]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    esquema = request.form.get('esquema')
    server_file = request.form.get('serverFile')

    try:
        carpeta_configs = crear_carpeta_configs()

        if server_file:
            file_path = os.path.join(carpeta_configs, server_file)
            if not os.path.exists(file_path):
                return jsonify({"error": "El archivo no existe en la carpeta 'Configs'"}), 400
            excel_file = pd.ExcelFile(file_path)
        else:
            if 'file' not in request.files:
                return jsonify({"error": "No se adjuntó ningún archivo"}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "El archivo no tiene nombre"}), 400
            excel_file = pd.ExcelFile(file)

        hojas = excel_file.sheet_names
        output_file = os.path.join(carpeta_configs, 'script_inserts.sql')
        with open(output_file, 'w', encoding='utf-8') as f:
            for hoja in hojas:
                f.write(f"-- SCRIPT '{hoja}'\n\n")
                tabla = pd.read_excel(excel_file, sheet_name=hoja)
                
                tabla = homogeneizar_columnas(tabla)

                for _, row in tabla.iterrows():
                    valores = ', '.join([formatear_valor(row[col]) for col in tabla.columns])
                    f.write(f"INSERT INTO {esquema}.{hoja} ({', '.join(tabla.columns)}) VALUES ({valores});\n")
                f.write('\n')

            for hoja in hojas:
                f.write(f"\n-- ROLLBACK '{hoja}'\n")
                tabla = pd.read_excel(excel_file, sheet_name=hoja)
                
                tabla = homogeneizar_columnas(tabla)

                columnas_para_condicion = tabla.columns[:2]  
                for _, row in tabla.iterrows():
                    condiciones = ' AND '.join([f"{col} = {formatear_valor(row[col])}" for col in columnas_para_condicion])
                    f.write(f"DELETE FROM {esquema}.{hoja} WHERE {condiciones};\n")

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def homogeneizar_columnas(tabla):

    for columna in tabla.columns:
        if tabla[columna].apply(lambda x: isinstance(x, str)).any():
            tabla[columna] = tabla[columna].astype(str)
        elif tabla[columna].apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x)).all():
            tabla[columna] = tabla[columna].astype(float) if tabla[columna].dtype == 'float64' else tabla[columna].astype(int)
    return tabla

def formatear_valor(valor, formato_fecha='YYYY-MM-DD'):
    if isinstance(valor, str):
        if valor.upper() in ['SYSDATE', 'CURRENT_DATE', 'CURRENT_TIMESTAMP']:
            return valor.upper()
        return f"'{valor.replace("'", "''")}'"
    elif isinstance(valor, datetime):
        if pd.isna(valor): 
            return 'NULL'
        if formato_fecha == 'DD-MM-YYYY':
            return f"TO_DATE('{valor.strftime('%d-%m-%Y')}', 'DD-MM-YYYY')"
        else:
            return f"TO_DATE('{valor.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')"    
    elif pd.isna(valor):
        return 'NULL'    
    elif isinstance(valor, (int, float)):
        if isinstance(valor, float) and valor.is_integer():
            return str(int(valor))
        else:
            return str(valor)
    else:
        return str(valor)

if __name__ == '__main__':
    app.run(debug=True, port=6969)
