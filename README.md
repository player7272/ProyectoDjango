# 🏢 BMS Soluciones Tecnológicas - Sistema de Gestión de Recursos Humanos

Sistema integral de gestión de recursos humanos desarrollado con Django, que incluye gestión de empleados, nóminas, permisos y solicitudes de empleo.

## 📋 Características Principales

- **Portal Público**: Página de inicio con información de la empresa y formulario de postulación
- **Portal de Empleados**: Dashboard personal, consulta de nóminas, solicitud de permisos
- **Portal de RRHH**: Gestión completa de empleados, nóminas, permisos y solicitudes
- **Sistema de Nóminas**: Cálculo automático de nóminas con deducciones configurables
- **Gestión de Permisos**: Solicitud y aprobación de permisos laborales
- **Reportes y Estadísticas**: Dashboard con métricas clave de recursos humanos

## 🛠️ Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## 📦 Instalación

### 1. Clonar o Descargar el Proyecto

```bash
# Si tienes Git instalado
git clone <url-del-repositorio>
cd ProyectoDjango

# O descarga el ZIP y descomprime
```

### 2. Crear un Entorno Virtual

**En Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install django
```

### 4. Configurar la Base de Datos

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate
```

### 5. Crear un Superusuario (Administrador)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu cuenta de administrador:
- Username: admin (o el que prefieras)
- Email: admin@bms.com (o el que prefieras)
- Password: (elige una contraseña segura)

### 6. Poblar la Base de Datos con Datos de Prueba

```bash
python manage.py shell < populate_db.py
```

Este script creará:
- ✅ 6 categorías de empleados
- ✅ 30 empleados con diferentes roles
- ✅ 120+ nóminas (4 meses de historial)
- ✅ 45+ permisos (aprobados, rechazados y pendientes)
- ✅ 25+ solicitudes de empleo
- ✅ Estados del sistema
- ✅ Tipos de permisos
- ✅ Configuración de nómina

### 7. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 🚀 Acceso al Sistema

### Portal Público
- **URL**: `http://127.0.0.1:8000/`
- Aquí podrás ver información de la empresa y postularte para un empleo

### Portal de Empleados
- **URL**: `http://127.0.0.1:8000/empleados/`
- **Credenciales de prueba**:
  - Usuario: `maria.garcia@bms.com` | Contraseña: `1234567890`
  - Usuario: `carlos.lopez@bms.com` | Contraseña: `0987654321`
  - Usuario: `ana.martinez@bms.com` | Contraseña: `1122334455`
  
  (Todos los empleados generados tienen como contraseña su número de cédula)

### Portal de Recursos Humanos
- **URL**: `http://127.0.0.1:8000/rrhh/`
- **Credenciales**: Tu cuenta de superusuario (creada en el paso 5)

### Panel de Administración Django
- **URL**: `http://127.0.0.1:8000/admin/`
- **Credenciales**: Tu cuenta de superusuario

## 📁 Estructura del Proyecto

```
ProyectoDjango/
├── core1/              # Portal público y solicitudes
│   ├── models.py       # Modelos: Persona, Solicitud, Categoría
│   ├── views.py        # Vistas del portal público
│   └── templates/      # Plantillas HTML
├── core2/              # Portal de empleados
│   ├── models.py       # Modelos: Empleado, Permiso, Nómina
│   ├── views.py        # Vistas del portal de empleados
│   └── templates/      # Plantillas HTML
├── core3/              # Portal de RRHH
│   ├── models.py       # Modelos: ProcesoContratación, Configuración
│   ├── views.py        # Vistas de recursos humanos
│   └── templates/      # Plantillas HTML
├── Static/             # Archivos estáticos (CSS, JS, imágenes)
│   ├── CSS/
│   ├── js/
│   └── img/
├── mysite/             # Configuración del proyecto
│   ├── settings.py     # Configuración de Django
│   └── urls.py         # Rutas principales
├── manage.py           # Script de gestión de Django
├── populate_db.py      # Script para poblar la BD
└── README.md           # Este archivo
```

## 🎯 Funcionalidades por Módulo

### Core1 - Portal Público
- Página de inicio con información de la empresa
- Formulario de postulación a empleos
- Consulta del estado de solicitud
- Listado de categorías disponibles

### Core2 - Portal de Empleados
- Dashboard personal con resumen
- Consulta de nóminas (historial completo)
- Solicitud de permisos
- Actualización de perfil personal
- Vista detallada de cada nómina

### Core3 - Portal de RRHH
- Dashboard con estadísticas clave
- Gestión de solicitudes de empleo
- Revisión y aprobación de permisos
- Gestión completa de empleados
- Creación y gestión de nóminas
- Generación automática de nóminas por periodo
- Reportes y estadísticas detalladas
- Configuración de parámetros de nómina

## 💡 Usuarios de Prueba Destacados

| Nombre | Email | Cédula (Password) | Categoría | Rol |
|--------|-------|-------------------|-----------|-----|
| María García | maria.garcia@bms.com | 1234567890 | Desarrollador Senior | Empleado |
| Carlos López | carlos.lopez@bms.com | 0987654321 | Gerente de Proyectos | Empleado |
| Ana Martínez | ana.martinez@bms.com | 1122334455 | Analista de Datos | Empleado |
| Luis Rodríguez | luis.rodriguez@bms.com | 5544332211 | DevOps Engineer | Empleado |

**Nota**: La contraseña de cada empleado es su número de cédula.

## 🔧 Configuración Adicional

### Cambiar el Puerto del Servidor

```bash
python manage.py runserver 8080
```

### Acceder desde Otros Dispositivos en la Red

```bash
python manage.py runserver 0.0.0.0:8000
```

Luego accede desde otro dispositivo usando la IP de tu máquina: `http://192.168.x.x:8000/`

### Limpiar la Base de Datos

```bash
# Eliminar la base de datos
del db.sqlite3  # Windows
rm db.sqlite3   # macOS/Linux

# Volver a crear
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < populate_db.py
```

## 🎨 Personalización

### Cambiar los Colores del Tema

Edita los archivos CSS en `Static/CSS/`:
- `style.css` - Estilos generales y tema
- `button.css` - Estilos de botones
- `cards.css` - Estilos de tarjetas
- `form.css` - Estilos de formularios
- `table.css` - Estilos de tablas

### Modificar el Logo

Reemplaza el archivo `Static/img/Logo.jpg` con tu propio logo (mismo nombre).

## 📊 Datos Generados por el Script

El script `populate_db.py` crea:

- **6 Categorías de Empleados**:
  - Desarrollador Junior ($2,000,000)
  - Desarrollador Senior ($4,000,000)
  - Analista de Datos ($3,500,000)
  - Gerente de Proyectos ($5,000,000)
  - DevOps Engineer ($3,800,000)
  - Diseñador UX/UI ($3,000,000)

- **30 Empleados** distribuidos en las categorías

- **4 Tipos de Permisos**:
  - Vacaciones (15 días máximo)
  - Permiso Médico (10 días máximo)
  - Permiso Personal (5 días máximo)
  - Permiso de Estudio (sin límite)

- **Nóminas**: 4 meses de historial para cada empleado

- **Permisos**: Variedad de permisos en diferentes estados

- **Solicitudes**: 25 solicitudes de empleo en diferentes estados

## 🐛 Solución de Problemas

### Error: "No module named 'django'"

```bash
pip install django
```

### Error: "Port already in use"

Detén cualquier servidor Django corriendo o usa otro puerto:
```bash
python manage.py runserver 8080
```

### Error al ejecutar populate_db.py

Asegúrate de que las migraciones estén aplicadas:
```bash
python manage.py migrate
```

### Los estilos no se cargan

Verifica que la carpeta `Static` esté en el directorio raíz del proyecto y ejecuta:
```bash
python manage.py collectstatic --noinput
```

## 📝 Notas Importantes

- Este es un proyecto de **demostración/desarrollo**, no está configurado para producción
- Las contraseñas de los usuarios de prueba son simples (números de cédula)
- Los datos generados son ficticios y para propósitos de demostración
- El modo DEBUG está activado en `settings.py` (desactivar en producción)

## 🔐 Seguridad en Producción

Si vas a desplegar este proyecto en producción, recuerda:

1. Cambiar `DEBUG = False` en `settings.py`
2. Configurar `ALLOWED_HOSTS` apropiadamente
3. Cambiar el `SECRET_KEY` por uno seguro
4. Usar una base de datos robusta (PostgreSQL, MySQL)
5. Configurar HTTPS
6. Implementar políticas de contraseñas fuertes
7. Configurar respaldos automáticos de la base de datos

## 🤝 Contribuciones

Este es un proyecto educativo/demostrativo. Si encuentras errores o tienes sugerencias, siéntete libre de reportarlos.

## 📄 Licencia

Proyecto desarrollado con fines educativos.

## 👥 Créditos

Desarrollado por: BMS Soluciones Tecnológicas
Framework: Django 5.2.7
Fecha: 2025

---

## 🚀 ¡Inicio Rápido!

```bash
# 1. Crear entorno virtual
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # macOS/Linux

# 2. Instalar Django
pip install django

# 3. Configurar base de datos
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Poblar con datos de prueba
python manage.py shell < populate_db.py

# 6. Ejecutar servidor
python manage.py runserver
```

¡Listo! Accede a `http://127.0.0.1:8000/` 🎉