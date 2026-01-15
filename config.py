class Config:
    """Configuración de la aplicación"""
    
    # Clave secreta para sesiones (cambiar en producción)
    SECRET_KEY = 'tu-clave-secreta-super-segura-123'
    
    # Configuración de MySQL (usando PyMySQL)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # Cambia esto por tu usuario de MySQL
    MYSQL_PASSWORD = ''  # Cambia esto por tu contraseña de MySQL
    MYSQL_DB = 'softura_productos'