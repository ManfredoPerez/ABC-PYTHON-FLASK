from flask import Flask, render_template, make_response, jsonify, request, send_file
from psycopg2 import connect, extras
from io import BytesIO
import matplotlib.pyplot as plt
from cryptography.fernet import Fernet

app = Flask(__name__)
key = Fernet.generate_key()

host = 'localhost'
port = 5432
dbname = 'ingenieria'
user = 'postgres'
password = '123ramoselfego'



def get_db_connection():
    conn = connect(host=host, database=dbname,
                   user=user, password=password, port=port)
    return conn


@app.get('/api/users')
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM productos")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    descripcion = new_user['descripcion']
    precio = new_user['precio']
    cantidad = new_user['cantidad']
    categoria = new_user['categoria']
    descripcion_categoria = new_user['descripcion_categoria']
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO productos (descripcion, precio, cantidad, categoria, descripcion_categoria) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (descripcion, precio, cantidad, categoria, descripcion_categoria))
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_user)


@app.get('/api/users/<id>')
def get_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'Product not found'}), 404

    return jsonify(user)


@app.put('/api/users/<id>')
def update_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    new_user = request.get_json()
    descripcion = new_user['descripcion']
    precio = new_user['precio']
    cantidad = new_user['cantidad']
    categoria = new_user['categoria']
    descripcion_cate = new_user['descripcion_categoria']
    cur.execute("UPDATE productos SET descripcion = %s, precio = %s, cantidad = %s, categoria = %s, descripcion_categoria = %s WHERE id = %s RETURNING *",
                (descripcion, precio, cantidad, categoria, descripcion_cate, id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_user is None:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(updated_user)


@app.delete('/api/users/<id>')
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM productos WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(user)

@app.route('/datos_grafica_productos_categoria')
def datos_grafica_productos_categoria():
    # Conectamos a la base de datos
    conn = get_db_connection()

    # Creamos un cursor para ejecutar consultas SQL
    cur = conn.cursor()

    # Ejecutamos la consulta SQL para obtener la cantidad de productos por categoría
    cur.execute("SELECT categoria, COUNT(*) FROM productos GROUP BY categoria;")

    # Obtenemos los resultados de la consulta
    resultados = cur.fetchall()

    # Cerramos el cursor y la conexión a la base de datos
    cur.close()
    conn.close()

    # Creamos una lista con las etiquetas y los datos de la gráfica
    etiquetas = [r[0] for r in resultados]
    datos = [r[1] for r in resultados]

    # Creamos un diccionario con los datos de la gráfica
    datos_grafica = {
        'etiquetas': etiquetas,
        'datos': datos
    }

    # Devolvemos los datos de la gráfica en formato JSON
    return jsonify(datos_grafica)


@app.get('/')
def home():
    return send_file('static/index.html')


if __name__ == '__main__':
    app.run(debug=True)
