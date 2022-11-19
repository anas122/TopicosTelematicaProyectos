# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co - Camila Mejia Muñoz, cmejiam10@eafit.edu.co - Nicolás Peñuela Solarte, npenuelas@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Avance Proyecto 2
#
# 1. Breve descripción de la actividad
Realizar una aplicación monolítica no escalable desplegada en AWS, con nombre de dominio y certificado SSL válido.

## 1.1. Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Despliegue de la aplicación Moodle con Docker y nginx en la instancia de AWS. Asignación de un dominio propio con certificado SSL válido con Let's Encrypt.  
Implementación de un balanceador de cargas con Docker y nginx en una instancia de AWS, en la capa de aplicación del Moodle.  
Implementación de un servidor de base de datos con Docker en una instancia de AWS, conectado al Moodle.  
Implementación de un servidor para archivos con Docker en una instancia de AWS, conectado al Moodle.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Realizar una aplicación monolítica no escalable desplegada en DCA, con nombre de dominio y certificado SSL válido. Esta no funcionó debido a que los servidores Moodle no conectan con el NFS, puede ser por un problema de puertos.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizaron contenedores en Docker para la ejecución del proyecto, Nginx y MariaDB.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
AWS, Docker, Nginx y MariaDB.

## Cómo se compila y ejecuta.
Para compilar y ejecutar, se accede a la instancia correspondiente, luego se accede a la carpeta donde se encuentran los archivos de docker-compose y nginx y se ejecuta el siguiente comando `docker-compose up`

## Detalles del desarrollo.
1. Para comenzar se crean 5 máquinas virtuales en AWS de tipo ec2-micro y se habilita el tráfico HTTP y HTTPS para cada una, además, se habilitan los puertos de NFS y MariaDB.

2. Se asigna una IP elástica a la máquina virtual respectiva al balanceador de cargas.

3. Luego accedemos a Cloudfare donde se encuentra el dominio y configuramos el registro A que apuntará a la dirección IP elástica asignada a la instancia del balanceador de cargas. Más adelante se agregará el registro TXT.

4. Luego, accedemos al dominio en Freenom, en herramientas de gestión, servidores de nombres, seleccionamos la opción "Usar nameservers personalizados (introducir abajo)" y agregamos todos los NS que nos provee Cloudfare.

### 1. Servidor NFS

1. Para crear el servidor NFS se conecta a la instancia de AWS de la máquina asignada a este mismo.

2. Para comenzar se ejecutan los siguientes comandos:
```
sudo apt update
sudo apt install nfs-kernel-server
```

3. Se crea una carpeta para compartir archivos en el servidor NFS:
```
sudo mkdir -p /mnt/nfs_share
```

4. Se crean las reglas de seguridad:
```
sudo chown -R nobody:nogroup /mnt/nfs_share/
sudo chmod 777 /mnt/nfs_share/
```

5. Ingresamos al archivo /etc/exports:
```
sudo nano /etc/exports
```

Agregamos el siguiente comando al final del archivo:
```
/mnt/nfs_share 172.31.0.0/16(rw,sync,no_subtree_check,no_root_squash)
```

6. Exportamos el nuevo NFS:
```
sudo exportfs -a
```

7. Actualizamos las nuevas reglas del firewall:
```
sudo systemctl restart nfs-kernel-server
sudo ufw allow from 172.31.0.0/16 to any port nfs
sudo ufw allow 22
sudo ufw enable
sudo ufw status
```

### 2. Servidor de base de datos
1. Para crear el servidor de base de datos se conecta a la instancia de AWS de la máquina asignada a este mismo.

2. Para comenzar se ejecutan los siguientes comandos:
```
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
```

3. Clonamos el repositorio donde se encuentran los scripts:
```
git clone https://github.com/anas122/TopicosTelematicaProyectos.git
```

4. Se crea un directorio para el docker container:
```
sudo mkdir /home/ubuntu/db
```

5. Copiamos en este directorio los archivos del github:
```
cd TopicosTelematicaProyectos/AvanceProyecto2/db
sudo cp docker-compose.yml /home/ubuntu/db
```

6. Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker ubuntu
```

7. Corremos el contenedor docker:
```
cd /home/ubuntu/db
sudo docker-compose up
```

### 3. Servidores Moodle

1. Para crear el servidor de moodle se conecta a la instancia de AWS de la máquina asignada a este mismo.

2. Para comenzar se ejecutan los siguientes comandos:
```
sudo apt update
sudo apt install nfs-common -y
```

3. Ingresamos al archivo /etc/fstab:
```
sudo nano /etc/fstab
```

Agregamos el siguiente comando al archivo, teniendo en cuenta que la dirección IP es la correspondiente a la instancia asignada al servidor NFS:
```
172.31.25.63:/mnt/nfs_share /var/www/html nfs auto 0 0
```

4. Se conecta al servidor con el NFS:
```
sudo mount
```

5. Se instala docker.io, docker-compose y git:
```
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
```

6. Se clona el repositorio donde se encuentran los scripts:
```
git clone https://github.com/anas122/TopicosTelematicaProyectos.git
```

7. Se crea un directorio para el docker container:
```
sudo mkdir /home/ubuntu/moodle
```

8. Copiamos en este directorio los archivos del github:
```
cd TopicosTelematicaProyectos/AvanceProyecto2/moodle
sudo cp docker-compose.yml /home/ubuntu/moodle
```

9. Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker ubuntu
```

10. Corremos el contenedor docker:
```
cd /home/ubuntu/moodle
sudo docker-compose up
```

### 4. Balanceador de cargas

1. Para crear el balanceador de cargas se conecta a la instancia de AWS de la máquina asignada a este mismo.

2. Se instala certbot, letsencrypt y nginx. Para esto, se ejecutan los siguientes comandos:
```
sudo apt update  
sudo apt install snapd  
sudo snap install certbot --classic  
sudo apt install letsencrypt -y  
sudo apt install nginx -y
```

3. Se ingresa al archivo nginx.conf y se configura:
```
sudo nano /etc/nginx/nginx.conf
```

4. Se reemplaza todo el contenido por lo siguiente:
```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections  1024;  ## Default: 1024
}
http {
    server {
        listen  80 default_server;
        server_name _;
        location ~ /\.well-known/acme-challenge/ {
            allow all;
            root /var/www/letsencrypt;
            try_files $uri = 404;
            break;
        }
    }
}
```

5. Se guarda la configuración de nginx con los siguientes comandos:
```
sudo mkdir -p /var/www/letsencrypt
sudo nginx -t
sudo service nginx reload
```

6. Para pedir los certificados SSL se ejecutan los siguientes comandos:
```
sudo certbot --server https://acme-v02.api.letsencrypt.org/directory -d *.npenuela.tk --manual --preferred-challenges dns-01 certonly
```

Este último comando nos va a generar el código que debemos ingresar en el registro TXT en Cloudfare.

7. Creamos carpetas para los certificados:
```
mkdir /home/npenuelas/nginx
mkdir /home/npenuelas/nginx/ssl
```

8. Para hacer los registros se ejecutan los siguientes comandos:
```
sudo su
cp /etc/letsencrypt/live/npenuela.tk/* /home/npenuelas/nginx/ssl/
exit
```

9. Se instala docker, docker-compose y git con los siguientes comandos:
```
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
```

10. Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker npenuelas
sudo reboot
```

11. Clonamos el repositorio del curso de donde usaremos un archivo de configuración:
```
git clone https://github.com/st0263eafit/st0263-2022-2.git
cd st0263-2022-2/docker-nginx-wordpress-ssl-letsencrypt
sudo cp ssl.conf /home/npenuelas/moodle
cd
```

12. Ingresamos a la carpeta y creamos los siguientes archivos:
```
cd nginx
sudo touch docker-compose.yml
sudo touch nginx.conf
```

13. Entramos al archivo nginx.conf con el siguiente comando:
```
sudo nano nginx.conf
```

14. Añadimos el siguiente contenido, teniendo en cuenta que las direcciones IP de las líneas 10 y 11 corresponden a las instancias del moodle 1 y 2:
```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
  worker_connections  1024;  ## Default: 1024
}
http {
  upstream loadbalancer{
    server 54.83.87.19:80 weight=5;
    server 174.129.98.10:80 weight=5;
  }
  server {
    listen 80;
    listen [::]:80;
    server_name _;
    rewrite ^ https://$host$request_uri permanent;
  }
  server {
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;
    server_name _;
    # enable subfolder method reverse proxy confs
    #include /config/nginx/proxy-confs/*.subfolder.conf;
    # all ssl related config moved to ssl.conf
    include /etc/nginx/ssl.conf;
    client_max_body_size 0;
    location / {
      proxy_pass http://loadbalancer;
      proxy_redirect off;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Host $host;
      proxy_set_header X-Forwarded-Server $host;
      proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
}
```

13. Ingresamos al archivo docker-compose.yml con el siguiente comando:
```
sudo nano docker-compose.yml
```

14. Añadimos el siguiente contenido:
```
version: '3.1'
services:
  nginx:
    container_name: nginx
    image: nginx
    volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl
    - ./ssl.conf:/etc/nginx/ssl.conf
    ports:
    - 80:80
    - 443:443
```

15. Detenemos nginx con los siguientes comandos:
```
ps ax | grep nginx
netstat -an | grep 80
sudo systemctl disable nginx
sudo systemctl stop nginx
```

16. Por último, iniciamos Docker:
```
cd /home/npenuelas/nginx
sudo docker-compose up
```

## Detalles técnicos
Se usó AWS para desplegar las máquinas virtuales.  
Se usaron contenedores de Docker.  
Se usó Cerbot y Let's Encrypt para asignar un certificado SSL válido.  
Se usó Nginx como servidor web HTTP.  
Se usó NFS kernel server para hacer el servidor NFS.

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Docker, Nginx, MariaDB y AWS.

# IP o nombres de dominio en nube o en la máquina servidor.
IP pública de la máquina servidor del Moodle 1: 34.227.8.228
IP pública de la máquina servidor del Moodle 2: 34.229.13.172
IP pública de la máquina servidor del NFS: 54.167.2.242
IP pública de la máquina servidor de la base de datos: 54.173.119.180
IP elástica de la máquina servidor del balanceador de cargas: 3.213.103.162
Nombre de dominio: npenuela.tk
Dominio con certificación ssl: https://moodle.npenuela.tk

## Una mini guia de como un usuario utilizaría el software o la aplicación
El usuario puede acceder desde cualquier navegador al link https://moodle.npenuela.tk y disfrutar de la aplicación.

# Referencias:
## https://github.com/st0263eafit/st0263-2022-2.git
## https://github.com/anas122/TopicosTelematica/tree/main/Laboratorio4

#### versión README.md -> 1.0 (2022-noviembre)