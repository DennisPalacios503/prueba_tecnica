Módulo de Gestión de Biblioteca - Odoo 19
Implementación de un sistema para la gestión de catálogos de libros y control de préstamos.

-------------------Características Principales
Catálogo de Libros: Gestión de títulos, autores, ISBN y estados de disponibilidad.

Cálculo Automático: Implementación de campos computados para determinar los años transcurridos desde la publicación.

Gestión de Préstamos: Registro de préstamos vinculados a miembros de la biblioteca con validaciones de fechas.

Automatización (Cron): Tarea programada diaria para verificar libros vencidos y preparar notificaciones.

Integración con Productos: Sincronización con el modelo product.product para disponibilidad en otros módulos (como POS).

Seguridad: Definición de grupos de acceso para Usuarios y Administradores de la Biblioteca.



-------------------------------------- Requisitos e Instalación
Versión de Odoo: Diseñado y testeado específicamente para Odoo 19.0.

Dependencias: Requiere el módulo base mail y product.

Instalación:

Copiar la carpeta library_management en el directorio de custom_addons.

Actualizar la lista de aplicaciones en el modo desarrollador de Odoo.

Instalar el módulo desde la interfaz o mediante terminal:

PowerShell
python odoo-bin -d nombre_base_datos -i library_management



------------------------------- Estructura del Proyecto
models/: Definición de la lógica de negocio (library.book, library.loan).

views/: Archivos XML para la interfaz de usuario (Formularios, Listas, Búsquedas).

data/: Configuración de la tarea programada (Cron) y plantillas de correo.

security/: Definición de permisos y reglas de acceso (ACL).


------------------------------ Notas de Desarrollo (Puntos Clave)
Compatibilidad Odoo 19: Se eliminó el uso del campo obsoleto numbercall en las tareas programadas, optando por la configuración estándar de la versión 19.

Lógica de Negocio: El método create en los libros asegura que el producto relacionado sea marcado como disponible en el Punto de Venta automáticamente.
