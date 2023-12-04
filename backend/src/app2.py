from flask import Flask, request, json, jsonify, session
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import config
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)
CORS(app)

con=MySQL(app)

@app.route('/home', methods=['GET'])
def listar_productos_cliente():
    try:
        cursor=con.connection.cursor()
        sql='select * from productos'
        cursor.execute(sql)
        datos=cursor.fetchall()
        productos=[]
        for fila in datos:
            #print(fila)
            producto={'id_producto':fila[0],'imagen_producto':fila[1],'nombre_producto':fila[2], 
                      'descripcion_producto':fila[3], 'artista_producto': fila[4],'ano_producto':fila[5],
                      'precio_producto':fila[6], 'stock_producto':fila[7], 'estatus_producto':fila[8]}
            productos.append(producto)
        print(len(productos))
        print(type(productos))
        return jsonify({'productos':productos, 'mensaje':'Lista de Productos','exito':True})


    except Exception as ex:
        return jsonify({'mensaje': 'error {}'.format(ex), 'exito':False})
    
@app.route('/listarDiscos/<id_producto>', methods=['GET'])
def listar_productos(id_producto):
    try:
        cursor=con.connection.cursor()
        sql='select * from productos WHERE id_producto = {0}'.format(id_producto)
        cursor.execute(sql)
        datos=cursor.fetchone()
        print(datos)
        #productos=[]
        # for fila in datos:
        #     #print(fila)
        #     producto={'id_producto':fila[0],'imagen_producto':fila[1],'nombre_producto':fila[2], 
        #               'descripcion_producto':fila[3], 'artista_producto': fila[4],'ano_producto':fila[5],
        #               'precio_producto':fila[6], 'stock_producto':fila[7], 'estatus_producto':fila[8]}
        #     productos.append(producto)
        producto={'id_producto':datos[0],'imagen_producto':datos[1],'nombre_producto':datos[2], 
                      'descripcion_producto':datos[3], 'artista_producto': datos[4],'ano_producto':datos[5],
                      'precio_producto':datos[6], 'stock_producto':datos[7], 'estatus_producto':datos[8]}
        print(len(producto))
        print(type(producto))
        return jsonify({'producto':producto, 'mensaje':'Lista de Productos','exito':True})


    except Exception as ex:
        return jsonify({'mensaje': 'error {}'.format(ex), 'exito':False})
    
# @app.route('editarProducto/<id_producto>', methods=['POST'])
# def actualizarLibro(id_producto):
    
#     id_producto = request.json['id_producto']
#     imagen_producto = request.json['imagen_producto']
#     nombre_producto = request.json['nombre_producto']
#     descripcion_producto = request.json['descripcion_producto']
#     artista_producto = request.json['artista_producto']
#     ano_producto = request.json['ano_producto']
#     precio_producto = request.json['precio_producto']
#     stock_producto = request.json['stock_producto']
#     estatus_producto = request.json['estatus_producto']

    

    
@app.route('/registrar_producto',methods=['POST'])
def registrar_producto():
    try:
        producto = leer_producto_bd(request.json['id_producto'])

        if producto != None:
            return jsonify({'mensaje': 'Producto ya existe', 'exito':False})
        else:
            cursor=con.connection.cursor()
            sql="""INSERT INTO productos(id_producto,imagen_producto,nombre_producto,descripcion_producto,artista_producto,ano_producto,precio_producto,
            stock_producto,estatus_producto) 
            VALUES({0},'{1}','{2}','{3}','{4}',{5},{6},{7},{8})""".format(request.json['id_producto'],request.json['imagen_producto'],
            request.json['nombre_producto'],request.json['descripcion_producto'],request.json['artista_producto'],request.json['ano_producto'],request.json['precio_producto'],
            request.json['stock_producto'], request.json['estatus_producto'])
            print(sql)
            cursor.execute(sql)
            con.connection.commit()
        return jsonify({'mensaje':'Producto agregado con éxito','exito':True})


    except Exception as ex:
        return jsonify({'mensaje': 'error {}'.format(ex), 'exito':False})
    
def leer_producto_bd(id_producto):
    try:
        cursor=con.connection.cursor()
        sql='select * from productos where id_producto= {0}'.format(id_producto)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            producto={'id_producto':datos[0],'imagen_producto':datos[1],'nombre_producto':datos[2],'descripcion_producto':datos[3],
                    'artista_producto':datos[4],'ano_producto':datos[5],'precio_producto':datos[6],'stock_producto':datos[7],'estatus_producto':datos[8]}
            return producto
        else:
            return None


    except Exception as ex:
        return ex

@app.route('/eliminarDisco', methods=['POST'])
def eliminar_producto():
    try:
        producto = leer_producto_bd(request.json['id_producto'])

        if producto == None:
            return jsonify({'mensaje': 'Producto no existe', 'exito':False})
        else:
            cursor=con.connection.cursor()
            sql="""DELETE FROM productos WHERE id_producto = {0}""".format(request.json['id_producto'])
            cursor.execute(sql)
            con.connection.commit()
        return jsonify({'mensaje':'Producto agregado con éxito','exito':True})

    except Exception as ex:
        return ex
    

@app.route('/editarProducto', methods=['POST'])
def modificar_producto():
    try:
        producto = leer_producto_bd(request.json['id_producto'])

        cursor=con.connection.cursor()
        sql="""UPDATE productos SET imagen_producto='{1}',nombre_producto='{2}',descripcion_producto='{3}',artista_producto='{4}',ano_producto={5},precio_producto={6},stock_producto={7},estatus_producto={8} WHERE id_producto={0}""".format(request.json['id_producto'],request.json['imagen_producto'],
            request.json['nombre_producto'],request.json['descripcion_producto'],request.json['artista_producto'],request.json['ano_producto'],request.json['precio_producto'],
            request.json['stock_producto'],request.json['estatus_producto'])
        cursor.execute(sql)
        datos=cursor.fetchone()
        
        
        con.connection.commit()
        return jsonify({'mensaje':'Producto modificado con éxito','exito':True})
        
    except Exception as ex:
        return jsonify({'mensaje': 'error {}'.format(ex), 'exito':False})
    
# @app.route('/iniciar_sesion', methods=['GET','POST'])
# def iniciar_sesion():
#     if request.method == 'POST' and 'nombre_usuario' in request.json and 'contrasena_usuario' in request.json:
#         # Create variables for easy access
#         id_usuario = request.json['id_usuario']
#         nombre_usuario = request.json['nombre_usuario']
#         correo_usuario = request.json['correo_usuario']
#         contrasena_usuario = request.json['contrasena_usuario']
#         tipo_usuario = request.json['tipo_usuario']
#         # Retrieve the hashed password
#         hash = contrasena_usuario + app.secret_key
#         hash = hashlib.sha1(hash.encode())
#         contrasena_usuario = hash.hexdigest()

#         # Check if account exists using MySQL
#         cursor = con.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena_usuario = %s'.format(request.json['nombre_usuario'], request.json['contrasena_usuario']))
#         # Fetch one record and return the result
#         account = cursor.fetchone()
#          # If account exists in accounts table in out database
#         if account:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id_usuario'] = account['id_usuario']
#             session['nombre_usuario'] = account['nombre_usuario']
#             session['tipo_usuario'] = account['tipo_usuario']
#             # Redirect to home page
#             return 'Logged in successfully!'
#         else:
#             # Account doesnt exist or username/password incorrect
#             msg = 'Incorrect username/password!'
    # try:
    #     cursor=con.connection.cursor()
    #     sql=""""""
    #     return
    # except Exception as ex:
    #     return ex

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    try:
        print(request.json)
        usuario = leer_usuario_bd(request.json['nombre_usuario'], request.json['contrasena_usuario'])
        print(usuario)
        if usuario != None:
            

            return jsonify({'usuario': usuario,'mensaje': 'Inicio de sesión exitoso', 'exito':True})
        else:

            # cursor=con.connection.cursor()
            # sql="""INSERT INTO productos(id_producto,imagen_producto,nombre_producto,descripcion_producto,artista_producto,ano_producto,precio_producto,
            # stock_producto,estatus_producto) 
            # VALUES({0},'{1}','{2}','{3}','{4}',{5},{6},{7},{8})""".format(request.json['id_producto'],request.json['imagen_producto'],
            # request.json['nombre_producto'],request.json['descripcion_producto'],request.json['artista_producto'],request.json['ano_producto'],request.json['precio_producto'],
            # request.json['stock_producto'], request.json['estatus_producto'])
            # print(sql)
            # cursor.execute(sql)
            # con.connection.commit()
            return jsonify({'mensaje':'El usuario ingresado no existe','exito':False})

    except Exception as ex:
        
        return jsonify({'mensaje': 'error {}'.format(ex), 'exito':False})

def leer_usuario_bd(nombre_usuario, contrasena_usuario):
    try:
        cursor=con.connection.cursor()
        sql="""select * from usuarios where nombre_usuario= '{0}' AND contrasena_usuario = '{1}'""".format(nombre_usuario, contrasena_usuario)
        print(sql)
        cursor.execute(sql)
        datos=cursor.fetchone()
        print(datos)
        if datos != None:
            usuario={'id_usuario':datos[0],'nombre_usuario':datos[1],'correo_usuario':datos[2],
                    'tipo_usuario':datos[4]}
            return usuario
        else:
            return None


    except Exception as ex:
        print(ex)
        return ex
    
@app.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    try:
        print(request.json)
        usuario = leer_usuario_bddos(request.json['id_usuario'])
        print(usuario)
        if usuario != None:
            

            return jsonify({'usuario': usuario,'mensaje': 'Cierre de sesión exitoso', 'exito':True})
        else:

            # cursor=con.connection.cursor()
            # sql="""INSERT INTO productos(id_producto,imagen_producto,nombre_producto,descripcion_producto,artista_producto,ano_producto,precio_producto,
            # stock_producto,estatus_producto) 
            # VALUES({0},'{1}','{2}','{3}','{4}',{5},{6},{7},{8})""".format(request.json['id_producto'],request.json['imagen_producto'],
            # request.json['nombre_producto'],request.json['descripcion_producto'],request.json['artista_producto'],request.json['ano_producto'],request.json['precio_producto'],
            # request.json['stock_producto'], request.json['estatus_producto'])
            # print(sql)
            # cursor.execute(sql)
            # con.connection.commit()
            return jsonify({'mensaje':'El usuario ingresado no existe','exito':False})

    except Exception as ex:
        return jsonify({'mensaje': 'error {}'.format(ex), 'exito':False})
    
def leer_usuario_bddos(id_usuario):
    try:
        cursor=con.connection.cursor()
        sql="""select * from usuarios where id_usuario= {0}""".format(id_usuario)
        print(sql)
        cursor.execute(sql)
        datos=cursor.fetchone()
        print(datos)
        if datos != None:
            usuario={'id_usuario':datos[0],'nombre_usuario':datos[1],'correo_usuario':datos[2],
                    'tipo_usuario':datos[4]}
            return usuario
        else:
            return None


    except Exception as ex:
        print(ex)
        return ex
    
@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    try: 
        usuario = leer_usuario_bdtres(request.json['nombre_usuario'])
        if usuario!= None:
            return jsonify({'mensaje': 'Este usuario ya existe', 'exito':False})
        else:
            cursor=con.connection.cursor()
            sql="""INSERT INTO usuarios(id_usuario,nombre_usuario,correo_usuario,contrasena_usuario,tipo_usuario) 
            VALUES({0},'{1}','{2}','{3}',2)""".format(request.json['id_usuario'],request.json['nombre_usuario'],
            request.json['correo_usuario'],request.json['contrasena_usuario'],request.json['tipo_usuario'])
            print(sql)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Usuario registrado con éxito','exito':True})

    except Exception as ex:
        return jsonify({'mensaje': 'error {}'.format(ex), 'exito':False})

def leer_usuario_bdtres(nombre_usuario):
    try:
        cursor=con.connection.cursor()
        sql="""select * from usuarios where nombre_usuario= '{0}'""".format(nombre_usuario)
        print(sql)
        cursor.execute(sql)
        datos=cursor.fetchone()
        print(datos)
        if datos != None:
            usuario={'id_usuario':datos[0],'nombre_usuario':datos[1],'correo_usuario':datos[2],
                    'tipo_usuario':datos[4]}
            return usuario
        else:
            return None


    except Exception as ex:
        print(ex)
        return ex

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(debug=True)
