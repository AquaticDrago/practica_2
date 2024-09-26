from flask import Flask, render_template, request, jsonify
import mysql.connector
import pusher
import pytz
import datetime

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

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    return render_template("app.html")

# Página de usuarios
@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

# Guardar nuevo usuario y enviar evento a Pusher
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

        # Enviar el evento a Pusher para notificar a las otras ventanas
        pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {"usuario": Usuario})

        return f"Usuario {Usuario} guardado exitosamente", 200
    except mysql.connector.Error as err:
        return f"Error al guardar: {err}", 500
    finally:
        cursor.close()
        con.close()

# Ruta para registrar con argumentos GET
@app.route("/registrar", methods=["GET"])
def registrar():
    try:
        # Obtener los parámetros GET
        args = request.args
        con = get_db_connection()
        cursor = con.cursor()

        # Insertar en la base de datos
        sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena, Fecha_Registro) VALUES (%s, %s, %s)"
        val = (args["usuario"], args["contrasena"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
        cursor.execute(sql, val)
        con.commit()

        # Enviar evento a Pusher
        pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {"usuario": args["usuario"]})
        return args
    except mysql.connector.Error as err:
        return f"Error al registrar: {err}", 500
    finally:
        cursor.close()
        con.close()

# Buscar los usuarios desde la base de datos
@app.route("/buscar", methods=["GET"])
def buscar():
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
        registros = cursor.fetchall()
        
        # Estructurar la respuesta como JSON
        return jsonify(registros), 200
    except mysql.connector.Error as err:
        return f"Error al buscar: {err}", 500
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    app.run(debug=True)
