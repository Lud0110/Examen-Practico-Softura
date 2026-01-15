from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    """Crear conexión a la base de datos"""
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    """Página principal con lista de productos"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.nombre, p.cantidad, c.nombre as categoria
                FROM productos p
                INNER JOIN categorias c ON p.categoria_id = c.id
                ORDER BY p.id DESC
            """)
            productos = cursor.fetchall()
        return render_template('index.html', productos=productos)
    finally:
        connection.close()

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear nuevo producto"""
    if request.method == 'POST':
        # Validación de datos
        nombre = request.form.get('nombre', '').strip()
        cantidad = request.form.get('cantidad', '').strip()
        categoria_id = request.form.get('categoria_id', '').strip()
        
        # Validaciones
        errores = []
        if not nombre or len(nombre) < 3:
            errores.append('El nombre del producto debe tener al menos 3 caracteres')
        
        if not cantidad or not cantidad.isdigit() or int(cantidad) < 0:
            errores.append('La cantidad debe ser un número entero positivo')
        
        if not categoria_id or not categoria_id.isdigit():
            errores.append('Debe seleccionar una categoría válida')
        
        if errores:
            for error in errores:
                flash(error, 'danger')
            categorias = obtener_categorias()
            return render_template('crear.html', categorias=categorias, nombre=nombre, cantidad=cantidad)
        
        # Insertar producto
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO productos (nombre, cantidad, categoria_id) VALUES (%s, %s, %s)",
                    (nombre, int(cantidad), int(categoria_id))
                )
                connection.commit()
            connection.close()
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error al crear el producto: {str(e)}', 'danger')
    
    categorias = obtener_categorias()
    return render_template('crear.html', categorias=categorias)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Editar producto existente"""
    connection = get_db_connection()
    
    if request.method == 'POST':
        # Validación de datos
        nombre = request.form.get('nombre', '').strip()
        cantidad = request.form.get('cantidad', '').strip()
        categoria_id = request.form.get('categoria_id', '').strip()
        
        # Validaciones
        errores = []
        if not nombre or len(nombre) < 3:
            errores.append('El nombre del producto debe tener al menos 3 caracteres')
        
        if not cantidad or not cantidad.isdigit() or int(cantidad) < 0:
            errores.append('La cantidad debe ser un número entero positivo')
        
        if not categoria_id or not categoria_id.isdigit():
            errores.append('Debe seleccionar una categoría válida')
        
        if errores:
            for error in errores:
                flash(error, 'danger')
            categorias = obtener_categorias()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
                producto = cursor.fetchone()
            connection.close()
            return render_template('editar.html', producto=producto, categorias=categorias)
        
        # Actualizar producto
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE productos SET nombre = %s, cantidad = %s, categoria_id = %s WHERE id = %s",
                    (nombre, int(cantidad), int(categoria_id), id)
                )
                connection.commit()
            connection.close()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            connection.close()
            flash(f'Error al actualizar el producto: {str(e)}', 'danger')
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
            producto = cursor.fetchone()
        
        if not producto:
            connection.close()
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('index'))
        
        categorias = obtener_categorias()
        return render_template('editar.html', producto=producto, categorias=categorias)
    finally:
        connection.close()

@app.route('/eliminar/<int:id>')
def eliminar(id):
    """Eliminar producto"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
            connection.commit()
        connection.close()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el producto: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    """Buscar productos"""
    productos = []
    termino = ''
    
    if request.method == 'POST':
        termino = request.form.get('termino', '').strip()
        
        if termino:
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT p.id, p.nombre, p.cantidad, c.nombre as categoria
                        FROM productos p
                        INNER JOIN categorias c ON p.categoria_id = c.id
                        WHERE p.nombre LIKE %s OR c.nombre LIKE %s
                        ORDER BY p.id DESC
                    """, (f'%{termino}%', f'%{termino}%'))
                    productos = cursor.fetchall()
            finally:
                connection.close()
    
    return render_template('buscar.html', productos=productos, termino=termino)

def obtener_categorias():
    """Obtener todas las categorías"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
            categorias = cursor.fetchall()
        return categorias
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)