from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de MongoDB
app.config["MONGO_URI"] = "mongodb+srv://cursor:kFd02zVLBS6daLqs@cluster0.63nwhve.mongodb.net/mimitos"
mongo = PyMongo(app)

# Configuración de Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'enzopiro80@gmail.com'
app.config['MAIL_PASSWORD'] = 'fkav idxk rhcv wyfw'  # Contraseña de aplicación
mail = Mail(app)

# Configuración de la aplicación
app.secret_key = "mimitos_secret_key_2024"

# Función para inicializar la base de datos con algunos productos de ejemplo
def init_db():
    # Primero eliminamos todos los productos existentes
    mongo.db.productos.delete_many({})
    
    productos_ejemplo = [
        {
            "nombre": "Alimento Premium para Perros Adultos",
            "descripcion": "Alimento balanceado para perros adultos, rico en proteínas y nutrientes esenciales",
            "precio": 29.99,
            "imagen": "https://i.imgur.com/8QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 100
        },
        {
            "nombre": "Alimento Premium para Gatos Adultos",
            "descripcion": "Alimento balanceado para gatos adultos, con taurina y nutrientes esenciales",
            "precio": 24.99,
            "imagen": "https://i.imgur.com/9QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 100
        },
        {
            "nombre": "Snacks Naturales para Perros",
            "descripcion": "Deliciosos snacks naturales para perros, sin conservantes artificiales",
            "precio": 9.99,
            "imagen": "https://i.imgur.com/7QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 150
        },
        {
            "nombre": "Juguete Interactivo para Gatos",
            "descripcion": "Juguete con plumas y sonajero para estimular el instinto de caza",
            "precio": 12.99,
            "imagen": "https://i.imgur.com/6QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 80
        },
        {
            "nombre": "Cama para Perros Mediana",
            "descripcion": "Cama suave y cómoda para perros medianos, fácil de lavar",
            "precio": 39.99,
            "imagen": "https://i.imgur.com/5QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 50
        },
        {
            "nombre": "Arena Aglomerante para Gatos",
            "descripcion": "Arena aglomerante de alta calidad, control de olores",
            "precio": 19.99,
            "imagen": "https://i.imgur.com/4QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 200
        },
        {
            "nombre": "Correa Retráctil para Perros",
            "descripcion": "Correa retráctil de 5 metros, con botón de bloqueo",
            "precio": 34.99,
            "imagen": "https://i.imgur.com/3QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 75
        },
        {
            "nombre": "Rascador para Gatos",
            "descripcion": "Rascador de sisal con plataforma y juguetes colgantes",
            "precio": 29.99,
            "imagen": "https://i.imgur.com/2QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 60
        },
        {
            "nombre": "Shampoo para Perros",
            "descripcion": "Shampoo hipoalergénico para perros, con acondicionador",
            "precio": 14.99,
            "imagen": "https://i.imgur.com/1QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 120
        },
        {
            "nombre": "Comedero Automático para Gatos",
            "descripcion": "Comedero automático programable, 4 comidas diarias",
            "precio": 49.99,
            "imagen": "https://i.imgur.com/0QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 40
        },
        {
            "nombre": "Juguete de Resistencia para Perros",
            "descripcion": "Juguete de caucho resistente para perros activos",
            "precio": 16.99,
            "imagen": "https://i.imgur.com/9QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 90
        },
        {
            "nombre": "Cepillo para Gatos",
            "descripcion": "Cepillo suave para eliminar pelo muerto",
            "precio": 11.99,
            "imagen": "https://i.imgur.com/8QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 100
        },
        {
            "nombre": "Collar Antipulgas para Perros",
            "descripcion": "Collar antipulgas y garrapatas, duración 8 meses",
            "precio": 24.99,
            "imagen": "https://i.imgur.com/7QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 150
        },
        {
            "nombre": "Transportadora para Gatos",
            "descripcion": "Transportadora segura y cómoda para gatos",
            "precio": 44.99,
            "imagen": "https://i.imgur.com/6QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 45
        },
        {
            "nombre": "Alimento para Perros Cachorros",
            "descripcion": "Alimento especial para cachorros, rico en calcio",
            "precio": 27.99,
            "imagen": "https://i.imgur.com/5QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 120
        },
        {
            "nombre": "Alimento para Gatos Cachorros",
            "descripcion": "Alimento especial para gatitos, con DHA",
            "precio": 22.99,
            "imagen": "https://i.imgur.com/4QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 120
        },
        {
            "nombre": "Cama para Gatos",
            "descripcion": "Cama suave y acogedora para gatos",
            "precio": 34.99,
            "imagen": "https://i.imgur.com/3QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 55
        },
        {
            "nombre": "Juguete de Peluche para Perros",
            "descripcion": "Peluche resistente para perros, sin relleno tóxico",
            "precio": 13.99,
            "imagen": "https://i.imgur.com/2QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 85
        },
        {
            "nombre": "Vitamina para Gatos",
            "descripcion": "Suplemento vitamínico para gatos adultos",
            "precio": 18.99,
            "imagen": "https://i.imgur.com/1QZQZQZ.jpg",
            "categoria": "gatos",
            "stock": 200
        },
        {
            "nombre": "Cepillo para Perros",
            "descripcion": "Cepillo profesional para perros de pelo largo",
            "precio": 15.99,
            "imagen": "https://i.imgur.com/0QZQZQZ.jpg",
            "categoria": "perros",
            "stock": 110
        }
    ]
    mongo.db.productos.insert_many(productos_ejemplo)

# Rutas públicas
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Número de productos por página
    productos = mongo.db.productos.find().skip((page - 1) * per_page).limit(per_page)
    total = mongo.db.productos.count_documents({})
    
    # Crear objeto de paginación
    class Pagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page
            self.has_prev = page > 1
            self.has_next = page < self.pages
            self.prev_num = page - 1
            self.next_num = page + 1

        def iter_pages(self, left_edge=2, left_current=2, right_current=3, right_edge=2):
            last = 0
            for num in range(1, self.pages + 1):
                if (num <= left_edge or
                    (num > self.page - left_current - 1 and
                     num < self.page + right_current) or
                    num > self.pages - right_edge + 1):
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

    pagination = Pagination(productos, page, per_page, total)
    return render_template('index.html', productos=pagination)

@app.route('/productos')
def productos():
    productos = list(mongo.db.productos.find())
    return render_template('productos.html', productos=productos)

@app.route('/producto/<id>')
def producto(id):
    producto = mongo.db.productos.find_one({"_id": ObjectId(id)})
    return render_template('producto.html', producto=producto)

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

# Rutas de autenticación
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if mongo.db.usuarios.find_one({'email': email}):
            flash('El correo electrónico ya está registrado', 'error')
            return redirect(url_for('registro'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('registro'))

        nuevo_usuario = {
            'nombre': nombre,
            'email': email,
            'password': generate_password_hash(password),
            'fecha_registro': datetime.now()
        }

        mongo.db.usuarios.insert_one(nuevo_usuario)
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = mongo.db.usuarios.find_one({'email': email})

        if usuario and check_password_hash(usuario['password'], password):
            session['usuario_id'] = str(usuario['_id'])
            session['nombre'] = usuario['nombre']
            flash('¡Bienvenido ' + usuario['nombre'] + '!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Correo electrónico o contraseña incorrectos', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('home'))

# Rutas del panel de administración
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    productos = list(mongo.db.productos.find())
    return render_template('admin/dashboard.html', productos=productos)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin'))
        flash('Credenciales inválidas')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/productos')
def admin_productos():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    productos = list(mongo.db.productos.find())
    return render_template('admin/productos.html', productos=productos)

@app.route('/admin/productos/nuevo', methods=['GET', 'POST'])
def admin_nuevo_producto():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        producto = {
            'nombre': request.form.get('nombre'),
            'precio': float(request.form.get('precio')),
            'imagen': request.form.get('imagen'),
            'categoria': request.form.get('categoria'),
            'descripcion': request.form.get('descripcion', ''),
            'stock': int(request.form.get('stock', 0))
        }
        mongo.db.productos.insert_one(producto)
        flash('Producto agregado exitosamente')
        return redirect(url_for('admin_productos'))
    return render_template('admin/nuevo_producto.html')

@app.route('/admin/productos/editar/<id>', methods=['GET', 'POST'])
def admin_editar_producto(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    producto = mongo.db.productos.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        mongo.db.productos.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                'nombre': request.form.get('nombre'),
                'descripcion': request.form.get('descripcion'),
                'precio': float(request.form.get('precio')),
                'imagen': request.form.get('imagen'),
                'categoria': request.form.get('categoria'),
                'stock': int(request.form.get('stock'))
            }}
        )
        flash('Producto actualizado exitosamente')
        return redirect(url_for('admin_productos'))
    return render_template('admin/editar_producto.html', producto=producto)

@app.route('/admin/productos/eliminar/<id>')
def admin_eliminar_producto(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    mongo.db.productos.delete_one({"_id": ObjectId(id)})
    flash('Producto eliminado exitosamente')
    return redirect(url_for('admin_productos'))

@app.route('/enviar_contacto', methods=['POST'])
def enviar_contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        
        mensaje_db = {
            'nombre': nombre,
            'email': email,
            'mensaje': mensaje,
            'fecha': datetime.now()
        }
        mongo.db.mensajes.insert_one(mensaje_db)
        
        msg = Message(
            subject=f'Nuevo mensaje de contacto de {nombre}',
            sender=email,
            recipients=['enzopiro80@gmail.com']
        )
        msg.body = f"""
        Nombre: {nombre}
        Email: {email}
        Mensaje: {mensaje}
        """
        mail.send(msg)
        
        flash('Mensaje enviado correctamente. Nos pondremos en contacto contigo pronto.')
        return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False) 