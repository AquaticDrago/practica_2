from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

# Configuración de la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id='1868790',
    key='e9dbf5518f64c87c2a78',
    secret='91c83b3f35c5203adbf1',
    cluster='us2',
    ssl=True
)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

@app.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    try:
        # Obtener la conexión a la base de datos
        con = get_db_connection()
        cursor = con.cursor()
        
        # Obtener los datos del formulario
        Usuario = request.form["txtUsuarioFA"]
        Contrasena = request.form["txtContrasenaFA"]

        # Insertar los datos en la base de datos
        sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
        cursor.execute(sql, (Usuario, Contrasena))
        con.commit()

        # Enviar el evento a Pusher
        pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {"usuario": Usuario})
        
        return f"Usuario {Usuario} guardado exitosamente", 200
    except mysql.connector.Error as err:
        return f"Error al guardar: {err}", 500
    finally:
        cursor.close()
        con.close()

@app.route("/buscar")
def buscar():
    try:
        # Obtener la conexión a la base de datos
        con = get_db_connection()
        cursor = con.cursor()

        # Consultar todos los usuarios ordenados por el ID
        cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
        registros = cursor.fetchall()

        # Convertir los registros a un formato JSON para enviarlos al frontend
        return jsonify(registros)
    except mysql.connector.Error as err:
        return f"Error al buscar: {err}", 500
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    app.run(debug=True)
