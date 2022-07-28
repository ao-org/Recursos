# Recursos
Recursos del cliente y el servidor de Argentum20, basado en RevolucionAO de Ladder


# Actualizaciones automaticas.

El archivo `version.php` es el encargado de crear el archivo http://parches.ao20.com.ar/files/Version.json que utiliza re20-lanzador para hacer la actualizacion. Se usa en el pipeline de Jenkins de crear parches.


El archivo `version_actualizar_steam.php` se utiliza para cambiar el ultimo build subido a Steam y hacerlo publico para que la gente se lo pueda bajar. Recordar poner `version_environment_steam.json` a mano con los valores correctos en el server de CI/CD


# Diagrama

<img src="https://i.ibb.co/vhXsMFx/AO20-drawio-2.png"/>
