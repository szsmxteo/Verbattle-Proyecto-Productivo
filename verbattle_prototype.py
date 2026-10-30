# VERBATTLE - PRODUCTO DE SOFTWARE (2026)
### Colegio León de Greiff I.E.D. - Programación para Dispositivos Móviles

---

## 🎮 Descripción del Proyecto
Verbattle es una plataforma web y móvil de gamificación orientada al aprendizaje dinámico de inglés y español mediante desafíos lingüísticos en tiempo real en salas virtuales 1vs1.

---

## 👥 Equipo de Trabajo
- **Product Owner (PO):** Johan Fabián Torres Parra
- **Scrum Master (SM):** Luigi Mateo Rubio Forero
- **Equipo de Desarrollo (Dev):** Kewin Alejandro Vásquez Ramírez, Oscar David Velasco Romero, Joel Nicolas Pirajan Gonzalez

---

## 📁 Estructura del Paquete (.ZIP)
1. `verbattle_django_project/`: Código fuente completo del servidor web en Django (MVT).
2. `verbattle_tkinter_prototype.py`: Prototipo de escritorio en Python/Tkinter.
3. `verbattle_database.sql`: Script DDL/DML para MySQL Server 8.0.
4. `recursos/`: Identidad gráfica oficial (Logos) y efectos de sonido.

---

## 🚀 Despliegue 100% Online (Sin Permisos de Administración)

### Opción 1: GitHub Codespaces
1. Clona el repositorio en GitHub.
2. Abre la pestaña `Codespaces` y selecciona `Create codespace on main`.
3. En la terminal integrada, ejecuta:
   ```bash
   cd verbattle_django_project
   python manage.py migrate
   python manage.py runserver
   ```

### Opción 2: PythonAnywhere
1. Sube este proyecto a tu cuenta en `pythonanywhere.com`.
2. Configura la base de datos MySQL con el archivo `verbattle_database.sql`.
3. Inicia la aplicación Web WSGI apuntando a `verbattle_config.wsgi`.
