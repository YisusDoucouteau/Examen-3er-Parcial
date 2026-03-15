# 🛠️ Sistema de Soporte Técnico con IA

Aplicación web desarrollada con **Flask** para la gestión de incidencias de soporte técnico dentro de una organización.

El sistema permite administrar **usuarios, categorías y tickets**, e integra **Inteligencia Artificial** para análisis de datos y consultas mediante lenguaje natural.

---

## 👥 Integrantes

- **Jesus Murillo** — Líder del proyecto / Backend / Integración IA  
- **Madeleine Vargas** — Módulo de Usuarios  
- **Elionai Paredes** — Módulo de Tickets  
- **Angel Mamani** — Módulo de Categorías  

---

## 🎯 Objetivo

Extender el sistema desarrollado previamente integrando **Inteligencia Artificial** para:

- Consultar información mediante un **chatbot**
- Analizar datos del sistema en un **dashboard inteligente**

---

## ⚙️ Tecnologías utilizadas

**Backend**
- Python
- Flask
- SQLAlchemy
- MySQL

**Visualización de datos**
- Chart.js

**Inteligencia Artificial**
- Groq API
- Modelo Llama 3

**Control de versiones**
- Git
- GitHub

---

## 🚀 Funcionalidades del sistema

### Gestión de Usuarios
- Crear usuarios
- Listar usuarios
- Editar usuarios
- Eliminar usuarios
- Control de roles (admin / usuario)

### Gestión de Categorías
- Crear categorías
- Listar categorías
- Editar categorías
- Eliminar categorías

### Gestión de Tickets
- Crear tickets
- Listar tickets
- Editar tickets
- Eliminar tickets
- Cambio de estado (abierto, en proceso, cerrado)

---

## 🤖 Chatbot Inteligente

El sistema incluye un **chatbot conectado a la base de datos** que permite hacer consultas usando lenguaje natural.

Ejemplos:

- ¿Cuántos tickets hay?
- ¿Cuántos tickets abiertos existen?
- ¿Qué categorías existen?
- ¿Cuál es la categoría con más incidencias?

El chatbot interpreta la pregunta, consulta la base de datos y genera una respuesta utilizando IA.

---

## 📊 Dashboard Inteligente

El dashboard muestra estadísticas del sistema como:

- Total de tickets
- Tickets abiertos, en proceso y cerrados
- Distribución de tickets por categoría

Además incluye **análisis automático generado por IA** para interpretar los datos del sistema.

---