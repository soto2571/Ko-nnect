# ko-nnect

ko-nnect es una aplicación web diseñada para facilitar la gestión de horarios y turnos de empleados. Con una interfaz intuitiva y características avanzadas, ko-nnect asegura que tanto empleados como administradores puedan gestionar y visualizar horarios de manera eficiente.

## Tabla de Contenidos

- [ko-nnect](#ko-nnect)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Instalación](#instalación)
  - [Uso](#uso)
  - [Características](#características)
  - [Contribución](#contribución)
  - [Licencia](#licencia)
  - [Contacto](#contacto)
    - [Equipo](#equipo)
  - [Historia y Agradecimientos](#historia-y-agradecimientos)

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo de ko-nnect:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/ko-nnect.git
   cd ko-nnect
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   Crea un archivo `.env` en la raíz del proyecto y añade las variables necesarias.

5. Realiza las migraciones de la base de datos:

   ```bash
   flask db upgrade
   ```

6. Inicia la aplicación:
   ```bash
   flask run
   ```

## Uso

Para iniciar la aplicación, asegúrate de que el entorno virtual esté activado y ejecuta:

```bash
flask run
```

## Características

- **Inicio de Sesión de Empleados:** Los empleados pueden iniciar sesión desde su teléfono o computadora para ver sus horarios al instante.
- **Calendario de Turnos y Festivos:** Visualiza un calendario de turnos hasta 3 semanas en adelante, incluyendo festivos en Puerto Rico.
- **Acceso Personalizado para Empleados:** Los administradores crean credenciales únicas para cada empleado, permitiéndoles acceder de manera segura a sus horarios.
- **Vista de Horarios de Dos Semanas:** Los empleados pueden ver una lista de sus turnos actuales y próximos durante los próximos 14 días.
- **Panel de Administración:** Un panel centralizado para que los administradores gestionen cuentas de empleados y horarios.

## Contribución

Si deseas contribuir a ko-nnect, sigue estos pasos:

1.  Haz un fork del repositorio.
2.  Crea una nueva rama (git checkout -b feature/nueva-caracteristica).
3.  Realiza tus cambios y haz commit (git commit -am 'Añadir nueva característica').
4.  Sube tus cambios (git push origin feature/nueva-caracteristica).
5.  Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto

Para más información, puedes contactaral equipo.

### Equipo

- [Sebastian Soto](https://github.com/soto2571)
- [Jose Mendez](https://github.com/jjmendezrodriguez)
- [Abdiel Rodriguez](https://github.com/Abdieljrg)

## Historia y Agradecimientos

Trabajar en ko-nnect ha sido una experiencia increíblemente gratificante para todos nosotros. Desde el inicio del proyecto, hemos aprendido y crecido tanto a nivel profesional como personal. La colaboración y el esfuerzo conjunto nos han permitido superar desafíos y alcanzar nuestros objetivos.

Queremos expresar nuestro más sincero agradecimiento a Holberton por brindarnos la educación y las herramientas necesarias para llevar a cabo este proyecto. Su apoyo y guía han sido fundamentales en nuestro desarrollo como desarrolladores de software.

**_¡Gracias, Holberton!_**
