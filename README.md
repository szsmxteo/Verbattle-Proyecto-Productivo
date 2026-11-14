# ⚡ VERBATTLE — Desafíos Lingüísticos 1vs1

> **Verbattle** es una plataforma gamificada de aprendizaje lingüístico orientada al público adolescente y gamer. Permite conectar a dos estudiantes en una sala virtual en tiempo real para resolver retos de vocabulario, velocidad y gramática en inglés y español.

---

## 🚀 Información del Proyecto Productivo
* **Institución:** Colegio León de Greiff I.E.D.
* **Especialidad:** Programación para Dispositivos Móviles
* **Año:** 2026
* **Metodología de Desarrollo:** Ágil — Scrum (Sprints semanales)

---

## 👥 Equipo de Trabajo y Organización por Ramas
| Integrante | Rol Scrum | Módulo / Rama Asignada |
| :--- | :--- | :--- |
| **Johan Fabián Torres Parra** | Product Owner (PO) | Controladores `views.py`, URLs, modelos ORM y Base de Datos (`rama-backend`) |
| **Luigi Mateo Rubio Forero** | Scrum Master (SM) | Interfaz móvil, maquetación visual, CSS y plantillas HTML (`rama-frontend`) |
| **Oscar David Velasco Romero** | Equipo de Desarrollo / QA | Pruebas unitarias de calidad y validación de formularios (`rama-testing`) |
| **Kewin Alejandro Vásquez Ramírez** | Equipo de Desarrollo / Docs | Documentación oficial del proyecto, actas y entregables (`rama-docs`) |

---

## 🛠️ Stack Tecnológico
* **Lenguajes:** Python 3.10+ / HTML5 / CSS3 / JavaScript
* **Framework Web:** Django 5.2 LTS (Arquitectura MVT)
* **Base de Datos:** SQLite en desarrollo / MySQL 8.0 (opcional, se activa desde `.env`)
* **Estilos Visuales:** Paleta e-sports (`#0D1B2A`, `#00E676`, `#00B4D8`) + Tipografía Montserrat
* **Prototipado:** Tkinter (Escritorio) / Figma (UI-UX)
* **Entorno y Control de Versiones:** Git & GitHub Codespaces

---

## 🎮 Funcionalidades Principales
1. **Lobby de Usuario:** Perfil de jugador, nivel de dominio (Bajo, Medio, Alto) y marcador de experiencia (XP).
2. **Arena 1vs1 (Pantalla Core):** Batallas en tiempo real con temporizador de 60 segundos y preguntas aleatorias.
3. **Gamificación:** Asignación de puntos XP, rachas de victorias y tabla de clasificación global.

---

## 💻 Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/szsmxteo/Verbattle-Proyecto-Productivo.git
cd Verbattle-Proyecto-Productivo
```

### 2. Prototipo de escritorio (Tkinter)
```bash
python verbattle_prototype.py
```

### 3. Aplicación web (Django)
```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env            # luego edita .env con tus datos

# Crear tablas y arrancar
python manage.py migrate
python manage.py runserver
```

---

## 🌿 Flujo de trabajo con ramas
1. Cada integrante trabaja en su rama (`rama-backend`, `rama-frontend`, `rama-testing`, `rama-docs`).
2. Al terminar una tarea, se abre un **Pull Request** hacia `main`.
3. Otro integrante revisa y aprueba antes de hacer merge.
4. Nadie hace `push` directo a `main`.

## 🧪 Pruebas
```bash
python manage.py test
```