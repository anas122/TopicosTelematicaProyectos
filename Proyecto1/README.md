# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co - Camila Mejia Muñoz, cmejiam10@eafit.edu.co - Nicolás Peñuela Solarte, npenuelas@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Proyecto 1
#
# 1. Breve descripción de la actividad
Implementación de una base de datos distribuida o un sistema de almacenamiento de archivos key,value, con particionamiento y replicación. Además, de permitir al cliente enviar peticiones CRUD a la base de datos a través de una API Sockets o HTTP.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Se desarrolló la base de datos distribuida o un sistema de almacenamiento de archivos key,value.  
Se logró implementar el CRUD con su respectivo client y server, a través de HTTP.  
Se implementó el particionamiento utilizando la libreria ray.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
No se logro la implementación de particionamiento físico, porque no creamos el algoritmo desde el principio, por el contrario, usamos una libreria de Python llamada ray la cual distribuye con su métodos.  
No se implementó la replicación.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizó ray y HTTP. La estructura que se buscó implementar fue de Cliente/Servidor, con particionamiento para la base de datos y el manejo de ellos, así como también buscar la replicación. Del alcance del proyecto, la arquitectura real consiste en una estructura Cliente/Servidor con particionamiento a través de una libreria, y con un sistema CRUD de base de datos con registros Key:Value.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Python 3.10.6  
Libreria requests 2.28.1 de HTTP  
Libreria pickle versión de Python 3.10.6  
Libreria urllib.parse versión de Python 3.10.6  
Libreria http.server versión de Python 3.10.6  
Libreria ray 2.0.0

## Como se compila y ejecuta.
1. Se instancian 3 máquinas virtuales Linux EC2 en AWS, una será el servidor, y las otras los clientes. En este caso las llamamos "Proyecto 1", "Cliente 1" y "Cliente 2". A todas las máquinas se les habilita el puerto 8080 en su grupo de seguridad.
2. En todas las máquinas se instala Python 3.10.6 y Ray 2.0.0.
3. En las máquinas "Proyecto 1" y "Cliente 1" se clona el repositorio https://github.com/anas122/TopicosTelematicaProyectos.git con el comando `git clone https://github.com/anas122/TopicosTelematicaProyectos.git` donde se encuentran los archivos de código que vamos a usar. (En este caso estos archivos se encuentran en una carpeta llamada "test", se puede acceder a ella usando el comando `cd test` y ejecutar los siguientes pasos desde aquí).
4. En la máquina "Proyecto 1" se ejecuta el comando `ray start --head`, cuando este se inicie nos indicará la dirección IP y el puerto en el que se encuentre.
5. En la máquina "Cliente 2" se ejecuta el comando `ray start --address='<Dirección IP:Puerto>'`, esta dirección IP y puerto se reemplazan con la información dada en el punto anterior. Con este comando este nodo se conectará al servidor.
6. Ahora, podemos realizar operaciones CRUD. En la máquina "Proyecto 1" se ejecuta el comando `python3 logic.py`, este indicará que el servidor ya está conectado.
7. En la máquina "Cliente 1" se ejecuta el comando `python3 app.py`, este desplegará un menu y se elegirá la opción de la operación que se desee realizar. Al terminar la operación se puede verificar el resultado y la respuesta en las máquinas "Cliente 1" y "Proyecto 1".

## Detalles del desarrollo.
Se configuraron tres instancias EC2 Linux, una es el servidor, y las otras los clientes. En el Servidor se ejecuta el comando de ray que inicializa el servidor para esperar requests de los clientes para manipular la base de datos. En los clientes se ejecuta un comando de Ray que permite al cliente comunicarse con el servidor a través de su IP, actuando como routing tier. Luego se ejecuta el archivo logic.py en el servidor, y el archivo app.py en el cliente en el que se vaya a hacer la prueba. Por la manera en que trabaja Ray, hace particionamiento mucho más escalable y facilita el procesamiento de las acciones que se vayan a realizar. Por lo que podría escalar el alcance del proyecto.  
Los parametros del proyecto son valores para añadir, borrar, o consultar datos en una base de datos con la forma Key:Value. Las direcciones IP son las que tienen cada instancia para poder hacer el enrutamiento al ejecutar, y la base de datos estaría en la instancia que actua como servidor, donde tiene un archivo llamado "dataBaseFile.dat" y almacena toda la información.

## Detalles técnicos
El archivo "app.py" se encarga de mostrarle una interfaz de usuario al cliente en modo de menu, para realizar las diferentes operaciones CRUD y envia las peticiones de cada operación al servidor.  
El archivo "logic.py" se encarga de realizar todas las operaciones CRUD y el particionamiento con ray.  
El archivo "constants.py" contiene los parametros estandar necesarios para el funcionamiento del programa, estos son usados por los archivos "app.py" y "logic.py".   
El archivo "dataBaseFile.dat" es el que usa el servidor para almacenar toda la información.

## Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
En todas las instancias se debe habilitar el puerto 8080. 

En el archivo "constants.py" se definieron todos los parametros:  
El filename es el nombre del archivo donde se guardará la información, en este caso "dataBaseFile.dat".  
Address es la dirección IP de localhost.  
Port es el puerto donde se ejecutarán los clientes y el servidor, en este caso el 8080.  
La url es para convertir el address y el port en una url accesible.

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Python 3.10.6    
Libreria ray 2.0.0

# IP o nombres de dominio en nube o en la máquina servidor.
IP elástica de la máquina servidor "Proyecto 1": 3.220.79.140  
IP elástica de la máquina cliente "Cliente 1": 34.194.9.46  
IP elástica de la máquina cliente "Cliente 2": 34.224.245.117

## Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
En todas las instancias se debe habilitar el puerto 8080.  
En el archivo "constants.py" están definidos todos los parametros, no se tienen que cambiar. 

## Como se lanza el servidor.
Para lanzar el servidor se ejecuta el comando `ray start --head` y luego `python3 logic.py`.

## Una mini guia de como un usuario utilizaría el software o la aplicación
1. Se instancian 3 máquinas virtuales Linux EC2 en AWS, una será el servidor, y las otras los clientes. En este caso las llamamos "Proyecto 1", "Cliente 1" y "Cliente 2". A todas las máquinas se les habilita el puerto 8080 en su grupo de seguridad.
2. En todas las máquinas se instala Python 3.10.6 y Ray 2.0.0.
3. En las máquinas "Proyecto 1" y "Cliente 1" se clona el repositorio https://github.com/anas122/TopicosTelematicaProyectos.git con el comando `git clone https://github.com/anas122/TopicosTelematicaProyectos.git` donde se encuentran los archivos de código que vamos a usar.
4. En la máquina "Proyecto 1" se ejecuta el comando `ray start --head`, cuando este se inicie nos indicará la dirección IP y el puerto en el que se encuentre.
5. En la máquina "Cliente 2" se ejecuta el comando `ray start --address='<Dirección IP:Puerto>'`, esta dirección IP y puerto se reemplazan con la información dada en el punto anterior. Con este comando este nodo se conectará al servidor.
6. Si se desean crear más nodos clientes se siguen los pasos 1 y 2 y se ejecuta el comando del paso anterior en este nuevo cliente para conectarse al servidor.
7. Ahora, podemos realizar operaciones CRUD. En la máquina "Proyecto 1" se ejecuta el comando `python3 logic.py`, este indicará que el servidor ya está conectado.
8. En la máquina "Cliente 1" se ejecuta el comando `python3 app.py`, este desplegará un menu y se elegirá la opción de la operación que se desee realizar. Al terminar la operación se puede verificar el resultado y la respuesta en las máquinas "Cliente 1" y "Proyecto 1".
9. Para realizar más operaciones CRUD se vuelve a ejecutar el comando `python3 app.py` en la máquina "Cliente 1" las veces que se desee, teniendo en cuenta que el servidor si esté corriendo.

# Referencias:
## https://docs.ray.io/en/latest/ray-overview/index.html

#### versión README.md -> 1.0 (2022-septiembre)