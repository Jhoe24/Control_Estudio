<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/sqlite-3.39-lightgrey?logo=sqlite&logoColor=white" alt="SQLite" />
</p>

<!-- Título principal -->
<h1 align="center">
  <span style="color:red;">🚀 Bienvenidos al Proyecto</span>
</h1>

Este archivo te guiará paso a paso para configurar el entorno de desarrollo y comenzar a trabajar en este proyecto sin problemas.

---

## <span style="color:red;">📋 Requisitos Previos</span>

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas:

- 🐍 **[Python](https://www.python.org/downloads/)** (última versión recomendada)  
- 📂 **[DB Browser for SQLite](https://sqlitebrowser.org/dl/)** (para visualizar la base de datos)  
- 🌳 **[Git](https://git-scm.com/downloads)** (para clonar el repositorio y control de versiones)  
- 🖥️ **[GitHub Desktop](https://desktop.github.com/download/)** (opcional, gestión visual)  
- 📝 **[Visual Studio Code](https://code.visualstudio.com/)** (editor recomendado)

> 🔔 **Nota:** Se recomienda usar GitHub Desktop o Git desde la terminal y VS Code para editar el código.

---

## <span style="color:red;">📥 Clonar el Repositorio</span>

Puedes usar GitHub Desktop o la terminal:

<details>
<summary>Con GitHub Desktop</summary>

En el menú **Archivo**, haga clic en **Clonar repositorio**. Haga clic en la pestaña correspondiente a la ubicación del repositorio que se desea clonar en nuestro caso "**Control_Estudio**". También puede hacer clic en **URL** para introducir manualmente la ubicación del repositorio (**https://github.com/Jhoe24/Control_Estudio.git**). En la lista de repositorios, haga clic en el repositorio que desea clonar.

</details>

<details>
<summary>Con la terminal</summary>

```bash
git clone https://github.com/Jhoe24/Control_Estudio.git
cd Control_Estudio
```
</details>

---

## <span style="color:red;">⚙️ Configuración del Entorno Virtual</span>

Sigue estos pasos para aislar tus dependencias y evitar conflictos con otros proyectos, tienes que estar dentro de la carpeta del proyecto (Control_Estudio) para crear el entorno virtual:

1. **Crear el entorno virtual**

   ```bash
   python -m venv env
   ```
2. **Activar el entorno virtual**

   * **Windows**

     ```bash
     .\env\Scripts\activate
     ```
   * **Linux/macOS**

     ```bash
     source env/bin/activate
     ```
---

## <span style="color:red;">📦 Instalación de Dependencias</span>

Con el entorno virtual activado, tienes dos opciones:

<details>
<summary>1. Usar <code>requirements.txt</code></summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary>2. Instalación manual</summary>

```bash
pip install customtkinter pillow tkcalendar sqlalchemy alembic reportlab openpyxl matplotlib pandas logging bcrypt
```

</details>

---

## <span style="color:red;">🚀 Ejecutar la Aplicación</span>

Una vez instaladas las dependencias:

```bash
# Puedes ejecutar el programa con los siguientes comandos
python .\main.py
# o tambien como 
py .\main.py 


```

---

## <span style="color:red;">📁 Estructura de Carpetas</span>

```text
.
├── 📦 controllers                   # Lógica de controladores
│   ├── controlador.py              # Controlador base
│   ├── forgotpasscontroller.py     # Gestión de recuperación de contraseña
│   ├── logincontroller.py          # Inicio de sesión
│   ├── masterController.py         # Funciones para usuarios master
│   └── registerController.py       # Registro de nuevos usuarios
│
├── 🔒 env/                          # Entorno virtual 
│
├── 🗄️ models                        # Modelos y esquemas de datos
│   ├── modelo.py                   # Modelo genérico
│   ├── modeloMaster.py             # Modelo para usuarios master
│   └── modeloUsuario.py            # Modelo de usuario
│
├── 🎨 src/                          # Recursos estáticos (imágenes, iconos)
│
├── 🛠️ util                          # Utilidades y helpers
│   ├── generic.py                  # Funciones genéricas
│   └── mensaje.py                  # Generador de mensajes
│
├── 📺 views                         # Plantillas y vistas
│   ├── admin                       
│   │   └── master_view.py          # Vista de administrador
│   │
│   ├── layouts.py                  
│   │   ├── admin_base.py           # Layout base admin
│   │   └── base.py                 # Layout base general
│   │
│   ├── forgotpassword_view.py      # Vista “Olvidé mi contraseña”
│   ├── login_view.py               # Vista de login
│   ├── newpassword_view.py         # Nueva contraseña
│   ├── register_view.py            # Registro de usuario
│   └── registerPreguntas_view.py   # Registro con preguntas de seguridad
│
├── .gitattributes                  # Atributos Git
├── .gitignore                      # Archivos ignorados
├── 🏁 main.py                       # Punto de entrada
├── 📄 README.md                     # Documentación principal
└── 📜 requirements.txt              # Dependencias / librerías
```

---

## <span style="color:red;">💡 Recomendaciones Adicionales</span>

* Instala en VS Code:

  * 🐍 **Python** (Microsoft)
  * 🔍 **Pylance**
  * 🔗 **SQLite Viewer**
  * 🖼️ **Material Icon Theme**

* Tambien puedes instalar cualquier otra extencion en vsCode que te pueda ayudar a desarrollar
* Haz commits frecuentes y sincroniza con GitHub.
* Mantén el entorno virtual activo mientras codificas.

---

<p align="center">  
  <img src="https://img.shields.io/badge/¡Listo_para_codificar!-🎉-brightgreen" alt="Ready to Code" />  
</p>
