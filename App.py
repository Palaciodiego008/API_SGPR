import re
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, request
from flask_mysqldb import MySQL
from models import clientes, convert_to_json, productos, convert_to_json_products
# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sgpr'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes

@app.route('/ping',methods=['GET'])
def ping():
    return jsonify({"data":"correcto"})

@app.route('/list_client',methods=['GET'])
def listaClientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    dato = cur.fetchall()
    cur.close()
    clientes = [ convert_to_json(cliente) for cliente in dato ]
    return jsonify({"cliente":clientes})

@app.route('/list_products',methods=['GET'])
def listaProductos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    dato = cur.fetchall()
    cur.close()
    productos = [ convert_to_json_products(producto) for producto in dato ]
    return jsonify({"producto":productos})


@app.route('/getAllById/<id>',methods=['GET'])
def getAllById(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    #print(data)
    return jsonify({"cliente":data})

@app.route('/getAllById_product/<id_producto>',methods=['GET'])
def getAllById_product(id_producto):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto))
    data = cur.fetchall()
    cur.close()
    return jsonify({"producto":data})



@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        nombre = request.json['nombre']
        telefono = request.json['telefono']
        direccion = request.json['direccion']
        num_documento = request.json['num_documento']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clientes (nombre, telefono, direccion, num_documento) VALUES (%s,%s,%s,%s)", (nombre, telefono, direccion, num_documento))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro exitoso"})

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        codigo_producto = request.json['codigo_producto']
        nombre_producto = request.json['nombre_producto']
        precio_producto = request.json['precio_producto']
        descripcion = request.json['descripcion']
        marca_producto = request.json['marca_producto']
        stock_producto = request.json['stock_producto']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (codigo_producto, nombre_producto, precio_producto, marca_producto,stock_producto, descripcion) VALUES (%s,%s,%s,%s,%s,%s)", (codigo_producto, nombre_producto, precio_producto,marca_producto, stock_producto,  descripcion))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro exitoso"})    

@app.route('/update_client/<id>', methods=['POST'])
def update_client(id):
    if request.method == 'POST':
        nombre = request.json['nombre']
        telefono = request.json['telefono']
        direccion = request.json['direccion']
        num_documento = request.json['num_documento']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET nombre = %s,
                telefono = %s,
                direccion = %s,
                num_documento = %s
            WHERE id = %s
        """, (nombre, telefono, direccion, num_documento, id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    
@app.route('/update_product/<id_producto>', methods=['POST'])
def update_product(id_producto):
    if request.method == 'POST':
        codigo_producto = request.json['codigo_producto']
        nombre_producto = request.json['nombre_producto']
        precio_producto = request.json['precio_producto']
        descripcion = request.json['descripcion']
        marca_producto = request.json['marca_producto']
        stock_producto = request.json['stock_producto']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE productos
            SET codigo_producto = %s,
                nombre_producto = %s,
                precio_producto = %s,
                descripcion = %s,
                marca_producto = %s,
                 stock_producto = %s
            WHERE id_producto = %s
        """, (codigo_producto, nombre_producto, precio_producto, descripcion,marca_producto, stock_producto, id_producto))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    
@app.route('/delete_product/<id_producto>', methods = ['GET'])
def delete_product(id_producto):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    mysql.connection.commit()
    return jsonify({"informacion":"Registro eliminado"})


@app.route('/delete_client/<id>', methods = ['GET'])
def delete_client(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id = %s', (id,))
    mysql.connection.commit()
    return jsonify({"informacion":"Registro eliminado"})


# starting the app
if __name__ == "__main__":
    app.run(port=4000, debug=True)
