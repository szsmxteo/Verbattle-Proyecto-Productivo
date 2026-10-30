# ⚡ VERBATTLE — Desafíos Lingüísticos 1vs1

<p align="center">
  <img src="recursos/LOGO_ESTANDAR_VERBATTLE.png" alt="Logo Verbattle" width="280"/>
</p>

> **Verbattle** es una plataforma gamificada de aprendizaje lingüístico orientada al público adolescente y gamer. Permite conectar a dos estudiantes en una sala virtual en tiempo real para resolver retos de vocabulario, velocidad y gramática en inglés y español.

---

## 🚀 Información del Proyecto Productivo
* **Institución:** Colegio León de Greiff I.E.D.
* **Especialidad:** Programación para Dispositivos Móviles
* **Año:** 2026
* **Metodología de Desarrollo:** Ágil — Scrum (Sprints semanales)

---

## 👥 Equipo de Trabajo
| Nombre Completo | Rol en el Proyecto |
| :--- | :--- |
| **Johan Fabián Torres Parra** | Product Owner (PO) |
| **Luigi Mateo Rubio Forero** | Scrum Master (SM) |
| **Kewin Alejandro Vásquez Ramírez** | Equipo de Desarrollo / UI-UX |
| **Oscar David Velasco Romero** | Equipo de Desarrollo / Backend |
| **Joel Nicolás Piraján González** | Equipo de Desarrollo / QA |

---

## 🛠️ Stack Tecnológico
* **Lenguajes:** Python 3.10+ / HTML5 / CSS3 / JavaScript
* **Framework Web:** Django 4.2 (Arquitectura MVT)
* **Base de Datos:** MySQL Server 8.0
* **Estilos Visuales:** Paleta e-sports (`#0D1B2A`, `#00E676`, `#00B4D8`) + Tipografía Montserrat
* **Prototipado:** Tkinter (Escritorio) / Figma (UI-UX)
* **Entorno y Control de Versiones:** Git & GitHub Codespaces

---

## 🎮 Funcionalidades Principales
1. **Lobby de Usuario:** Perfil de jugador, nivel de dominio (Bajo, Medio, Alto) y marcador de experiencia (XP).
2. **Arena 1vs1 (Pantalla Core):** Batallas en tiempo real con temporizador de 60 segundos y preguntas aleatorias.
3. **Gamificación:** Asignación de puntos XP, rachas de victorias y tabla de clasificación global.

---

## 💻 Cómo ejecutar el prototipo de escritorio (Tkinter)
```bash
# 1. Clonar el repositorio
git clone [suspicious link removed]

# 2. Entrar a la carpeta del proyecto
cd Verbattle-Proyecto-Productivo

# 3. Ejecutar el prototipo
python verbattle_prototype.py

3. **Guardar los cambios:**
   * Presiona `Ctrl + S` (o `Cmd + S` en Mac) para guardar el archivo.

---

### PASO 5: Publicar todo en GitHub desde la Terminal

Una vez guardado el `README.md`, ve a la **terminal** en la parte inferior de Codespaces y ejecuta estos 3 comandos en orden para enviar todos los archivos a GitHub:

```bash
git add .
git commit -m "Se configura la portada principal README.md, recursos y prototipo de Verbattle"
git push origin main