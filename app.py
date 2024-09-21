from flask import Flask
from markupsafe import escape

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
  
    return render_template("app.html")

@app.route("/usuarios")
def usuarios():
    con.close()
  
    return render_template("usuarios.html")

@app.route("/usuarios/guardar", methods=["POST"])
def usuariosGuardar():
    con.close()
  
    Usuario      = request.form["txtUsuarioFA"]
    Contrasena = request.form["txtContrasenaFA"]

    return f"Usuario: {matricula} Contrasena: {nombreapellido}"

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args
    pusher_client = pusher.Pusher(
      app_id='1868790',
      key='e9dbf5518f64c87c2a78',
      secret='91c83b3f35c5203adbf1',
      cluster='us2',
      ssl=True
    )

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    
    sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
    val = (args["nombre"], args["contrasena"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
    cursor.execute(sql, val)

    con.commit()
    con.close()
 
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", args)
    return args

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
    registros = cursor.fetchall()

    con.close()

    return registros
