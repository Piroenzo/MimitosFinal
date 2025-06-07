# Mimitos - Tienda de Alimentos para Mascotas

Tienda web especializada en la venta de alimentos para mascotas.

## Características
- Catálogo de productos
- Sistema de carrito de compras
- Registro y login de usuarios
- Panel de administración
- Base de datos MongoDB Atlas

## Tecnologías utilizadas
- Frontend: HTML, CSS
- Backend: Python (Flask)
- Base de datos: MongoDB Atlas

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```
   python -m venv venv
   ```
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
5. Configurar variables de entorno en un archivo `.env`
6. Ejecutar la aplicación:
   ```
   python app.py
   ```

## Estructura del proyecto
```
mimitos/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── app.py
├── requirements.txt
└── README.md
``` 