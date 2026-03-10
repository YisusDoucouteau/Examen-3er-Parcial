# 🛠️ Sistema de Soporte Técnico

Aplicación web desarrollada con Flask para la gestión de incidencias de soporte técnico dentro de una organización.
Permite administrar usuarios, categorías y tickets, con control de acceso por roles y exportación de reportes.

---

## 👥 Integrantes

* **Jesus Murillo** — Líder del proyecto / Backend principal / Integración
* **Madeleine Vargas** — Módulo de Usuarios
* **Elionai Paredes** — Módulo de Tickets
* **Angel Mamani** — Módulo de Categorías

---

## 🎯 Objetivo del sistema

Este sistema permite registrar, organizar y dar seguimiento a solicitudes de soporte técnico.

Los usuarios pueden reportar incidencias y el personal puede gestionarlas por estado y categoría.

---

## 🚀 Tecnologías utilizadas

* Python 3
* Flask
* Flask-Login (Autenticación)
* Flask-Migrate (Migraciones)
* SQLAlchemy (ORM)
* MySQL (Base de datos)
* Bootstrap 5 (Interfaz)
* OpenPyXL (Exportación a Excel)
* ReportLab (Exportación a PDF)
* Git & GitHub (Trabajo colaborativo)

---

## ⚙️ Instalación del proyecto

### 1️⃣ Clonar repositorio

```bash
git clone https://github.com/YisusDoucouteau/Examen-parcial-2-Grupo-6.git
cd Examen-parcial-2-Grupo-6
```

---

### 2️⃣ Crear entorno virtual

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🔐 Variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=clave_secreta
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_NAME=soporte_tecnico
```

---

## 🗄️ Base de datos

Crear la base de datos en MySQL:

```sql
CREATE DATABASE soporte_tecnico;
```

---

## 🔄 Migraciones

**Windows (PowerShell)**

```bash
$env:FLASK_APP="run.py"
flask db upgrade
```

**Mac / Linux**

```bash
export FLASK_APP=run.py
flask db upgrade
```

Esto creará todas las tablas automáticamente.

---

## ▶️ Ejecutar proyecto

```bash
python run.py
```

Abrir en navegador:

```
http://127.0.0.1:5000
```

---

## 🧩 Funcionalidades del sistema

### 👤 Gestión de Usuarios (Administrador)

* Crear usuarios
* Listar usuarios
* Editar usuarios
* Eliminar usuarios
* Validación de correo único
* Protección de seguridad:

  * Un administrador no puede eliminar su propia cuenta

---

### 🗂️ Gestión de Categorías

* Crear categoría
* Listar categorías
* Editar categoría
* Eliminar categoría
* Validación de nombre obligatorio
* Restricción:

  * No se puede eliminar una categoría con tickets asociados

---

### 🎫 Gestión de Tickets

* Crear ticket
* Listar tickets
* Editar ticket
* Eliminar ticket
* Cambio de estado:

  * Abierto
  * En proceso
  * Cerrado
* Filtro de tickets por estado

---

## 📊 Reto adicional implementado

### 📁 Exportación de reportes

Se implementaron dos tipos de exportación:

**Exportar todos los tickets a Excel**

* Genera un reporte completo para análisis administrativo
* Facilita control y estadísticas

**Exportar ticket individual a PDF**

* Genera una ficha detallada de un ticket específico
* Útil como comprobante o evidencia de atención

---

## 🔒 Control de acceso

* Inicio de sesión obligatorio
* Sistema de autenticación con Flask-Login
* Manejo de roles:

  * Administrador
  * Usuario normal
* Restricción de módulos según permisos

---

## 👨‍💻 Arquitectura del proyecto

El sistema está organizado por módulos usando Blueprints:

* `usuarios` → Gestión de cuentas
* `categorias` → Organización de incidencias
* `tickets` → Gestión de solicitudes de soporte

Esto permite mantener el código organizado y escalable.

---

## 🤝 Trabajo colaborativo

* Cada integrante trabajó en su propia rama
* Se usaron Pull Requests para integrar cambios
* Flujo profesional de control de versiones

---

## 🧠 Aprendizajes del proyecto

* Desarrollo de aplicaciones web con Flask
* Arquitectura modular
* Manejo de autenticación y roles
* Integración con bases de datos relacionales
* Exportación de datos en múltiples formatos
* Trabajo en equipo con Git y GitHub

---

## ⚠️ Dificultades encontradas

Durante el desarrollo del proyecto se presentaron algunos retos técnicos:

- Configuración del entorno y variables de entorno entre distintos equipos.
- Manejo de migraciones de base de datos en entornos locales.
- Control de versiones colaborativo usando ramas y Pull Requests.
- Implementación de restricciones lógicas, como evitar eliminar categorías con tickets asociados.
- Generación de archivos Excel y PDF desde datos dinámicos.
- Control de permisos para evitar que un administrador elimine su propia cuenta.

---

## 🛠️ Cómo se resolvieron

- Estandarizando pasos de instalación para todo el equipo.
- Uso de Flask-Migrate para control de cambios en la base de datos.
- Flujo Git con ramas individuales y revisión mediante Pull Requests.
- Implementación de validaciones en backend para proteger la integridad de datos.
- Uso de librerías especializadas:
  - OpenPyXL para exportación a Excel
  - ReportLab para generación de PDF