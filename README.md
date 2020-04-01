# SGDF
Sistema de Gestión de ficheros
Prueba: Sistema de gestión de ficheros
El objetivo de la prueba es crear un sistema de gestión de ficheros que cumpla con lo siguiente:
El sistema debe de estar compuesto por un interfaz web, un servicio de backend y una base de datos SQL.

Los usuarios deben de poder enviar ficheros mediante un formulario para su almacenamiento en el servidor.

Los ficheros almacenados deben de mostrarse en una lista ordenada en el frontal, con atributos como el nombre del fichero, la fecha de subida, el tamaño de los mismos, el hash sha256 de los mismos y la posibilidad de descargarlos o eliminarlos.

Debe de tener un sistema de gestión de identidades funcional: Se debe de poder acceder con dos tipos de usuario distintos con dos grados de visibilidad distintos. El usuario que tenga mayor nivel de privilegios debe de poder borrar los archivos almacenados.

El directorio a utilizar para el guardado de ficheros será "C:\SGDF" en Windows y "/opt/SGDF" en Linux.

La tecnología a utilizar debe ser la siguiente:
Python 3.6 para el servicio de backend.

Jinja 2 para las plantillas html.

Javascript para el control de interacciones en el lado cliente.

MariaDB o SQLite para la gestión de usuarios y de datos de ficheros.

Debe ser compatible con Windows 10 y Ubuntu Server 18.04.

Instrucciones adicionales:
Se comprobará su funcionamiento mediante la descarga y ejecución del archivo "main.py" de este repositorio.

En caso de necesitar librerías de terceros, se adjuntaran en un fichero "requirements.txt" para poder ser descargadas con pip.

Si se requieren paquetes adicionales a instalar en el sistema operativo, se indicaran en un fichero "leeme.txt".
