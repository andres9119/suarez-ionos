# Portal Institucional - Alcaldía Municipal de Suárez, Cauca

Este proyecto es un portal dinámico orientado a contenidos institucionales, construido con Django y Bootstrap.

## Requisitos
- Python 3.10+
- MySQL Server
- Entorno virtual (recomendado)

## Configuración Local

1.  **Clonar/Descargar el proyecto**
2.  **Configurar base de datos**:
    - **Desarrollo**: Por defecto, el proyecto usa **SQLite** cuando `DEBUG=True` en `settings.py`. No requieres configuración adicional para empezar.
    - **Producción**: Para usar MySQL, configura las variables en un archivo `.env`:
      ```env
      DB_NAME=suarez_db
      DB_USER=tu_usuario
      DB_PASSWORD=tu_contrasena
      DB_HOST=localhost
      DB_PORT=3306
      DEBUG=False
      ```
3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ejecutar migraciones**:
    ```bash
    python manage.py makemigrations
    ```
    *(Nota: Debes tener el servicio MySQL corriendo y los parámetros en .env correctos)*
5.  **Crear superusuario**:
    ```bash
    python manage.py createsuperuser
    ```
6.  **Iniciar el servidor**:
    ```bash
    python manage.py runserver
    ```

## Estructura de Apps
- `inicio`: Home, videos, galerías y eventos destacados.
- `noticias`: Blog de noticias y eventos municipales.
- `comunidades`: Reseñas culturales de comunidades indígenas, afro y campesinas.
- `experiencias_cafeteras`: Historias y procesos del café local.
- `documentos`: Repositorio de documentos públicos categorizados.
- `contacto`: Formulario de contacto para ciudadanos.

## Licencia
Este proyecto es de código abierto bajo la licencia MIT.
