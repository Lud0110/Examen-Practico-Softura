-- Script de creación de base de datos para el sistema de productos
-- Softura Solutions

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS softura_productos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE softura_productos;

-- Tabla de categorías de productos
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    cantidad INT NOT NULL DEFAULT 0,
    categoria_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar categorías de ejemplo
INSERT INTO categorias (nombre, descripcion) VALUES
('Electrónica', 'Productos electrónicos y tecnológicos'),
('Ropa', 'Prendas de vestir y accesorios'),
('Alimentos', 'Productos alimenticios'),
('Hogar', 'Artículos para el hogar'),
('Deportes', 'Equipamiento deportivo'),
('Libros', 'Libros y material de lectura'),
('Juguetes', 'Juguetes y juegos'),
('Salud', 'Productos de salud y cuidado personal');

-- Insertar productos de ejemplo
INSERT INTO productos (nombre, cantidad, categoria_id) VALUES
('Laptop HP', 15, 1),
('Mouse Inalámbrico', 50, 1),
('Camisa Formal', 30, 2),
('Pantalón de Mezclilla', 25, 2),
('Arroz 1kg', 100, 3),
('Aceite de Cocina', 75, 3),
('Silla de Oficina', 10, 4),
('Lámpara LED', 40, 4),
('Balón de Fútbol', 20, 5),
('Raqueta de Tenis', 12, 5);

-- Consultas de verificación
SELECT 'Categorías creadas:' as mensaje;
SELECT * FROM categorias;

SELECT 'Productos creados:' as mensaje;
SELECT p.id, p.nombre, p.cantidad, c.nombre as categoria 
FROM productos p 
INNER JOIN categorias c ON p.categoria_id = c.id;