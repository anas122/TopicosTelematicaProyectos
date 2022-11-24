# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co - Camila Mejia Muñoz, cmejiam10@eafit.edu.co - Nicolás Peñuela Solarte, npenuelas@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Proyecto 2
#
# 1. Breve descripción de la actividad
Despliegue de una aplicación open source con Moodle-vpl, funcionando en la nube AWS. Escalable, Robusto, Seguro, con nombre de dominio y certificado SSL válido, utilizando los servicios EC2, ELB, RDS y EFS.

## 1.1. Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Crear un Moodle template en las instancias de AWS.  
Crear una AMI del Moodle template y un target group.  
Crear una base de datos MariaDB con el servicio de RDS.  
Crear un servidor NFS en el servicio EFS.  
Crear un grupo auto escalable en AWS.  
Crear un balanceador de carga para las instancias con el servicio ELB.  
Asignar un certificado ssl válido al dominio.

## 1.2. Qué aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Todos los aspectos fueron cumplidos y desarrollados.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizaron contenedores Docker para el despliegue de las instancias, CloudFlare para el manejo del DNS y certificados SSL, instancias EC2 en AWS, servicio de AMI en AWS, base de datos MariaDB con el servicio RDS en AWS, servidor NFS con el servicio EFS en AWS, grupo de auto scaling en AWS y balanceador de cargas con el servicio ELB en AWS.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Docker, Moodle, CloudFlare, EC2 en AWS, servicio de AMI en AWS, MariaDB con el servicio RDS en AWS, EFS en AWS, grupo de auto scaling en AWS y ELB en AWS.

## Cómo se compila y ejecuta.
Para compilar y ejecutar, se accede a la instancia correspondiente, luego se accede a la carpeta donde se encuentran los archivos de docker-compose y se ejecuta el siguiente comando `docker-compose up`

## Detalles del desarrollo.
1. Iniciamos creando un grupo de seguridad para cada servicio que se va a usar.

2. Creamos un servidor NFS con el servicio EFS en AWS.

3. Creamos una base de datos MariaDB con el servicio RDS en AWS.

4. Lanzamos una instancia en EC2 en AWS que será nuestra plantilla a utilizar para el grupo de autoscaling.

![image](https://user-images.githubusercontent.com/37346028/203655088-957dfc8e-5eb3-4396-9fa4-9780dd42e007.png)

5. Le asignamos nombre a la instancia plantilla, elegimos el OS.

![image](https://user-images.githubusercontent.com/37346028/203655210-4ee97374-b591-445f-b1a9-403e84d5ac13.png)

6. Elegimos t2.micro, y también asignamos el par de claves vockey por defecto.

![image](https://user-images.githubusercontent.com/37346028/203655575-10ba667d-6ef4-4831-b331-e80f61d43619.png)

7. En configuración de red, elegimos “Seleccionar un grupo de seguridad existente, y elegimos el grupo de seguridad que creamos previamente para el webserver del Moodle. También elegimos en la subred de la VPC default, la zona “us-east-1a“ que es la zona en donde creamos el EFS.

![image](https://user-images.githubusercontent.com/37346028/203655911-7b4f3305-9cb9-487b-9b59-9270765eed83.png)

8. Luego, en los volúmenes, seleccionamos el EFS que creamos previamente y configuramos el punto de montaje a “/mnt/moodle/

![image](https://user-images.githubusercontent.com/37346028/203656155-61b4069f-1c0a-4c44-a2bd-af74f009374e.png)

9. Desactivamos la primera casilla, y lanzamos la instancia.

![image](https://user-images.githubusercontent.com/37346028/203656253-a9837242-5b30-43c7-8218-613d5a190f31.png)

10. Entramos a la instancia creada y corremos el comando mount para revisar que el EFS esté configurado correctamente.

![image](https://user-images.githubusercontent.com/37346028/203656392-7e52357e-9ce3-440d-94cf-f100b02c2fbf.png)

11. Ejecutamos los siguientes comandos:
```
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo mkdir moodle
cd moodle
sudo apt install git -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker ubuntu
sudo apt install mysql-client
mysql -u userp2 -h database-1.cnki7bnyetjm.us-east-1.rds.amazonaws.com -p
```

12. Entramos al cliente mysql y creamos la base de datos en el servicio RDS previamente configurado.

![image](https://user-images.githubusercontent.com/37346028/203656701-951b4a76-9131-4632-a19e-3446f14c8696.png)

13. Creamos la base de datos “bitnami_moodle” para utilizar en el proyecto.

![image](https://user-images.githubusercontent.com/37346028/203656844-8777d1a8-bf31-457b-8d7b-035d55a012ec.png)

14. Creamos el docker-compose.yml, insertando los datos de la base de datos que esta en RDS.

![image](https://user-images.githubusercontent.com/37346028/203656937-233671b7-0181-4816-b8f2-8754642ff801.png)

15. Ejecutamos el compose up y creamos el contenedor.

![image](https://user-images.githubusercontent.com/37346028/203657052-8e6e443b-a728-4085-9dec-7ec891e6d9e8.png)

16. Probamos con la IP pública de la máquina que esté funcionando el Moodle.

![image](https://user-images.githubusercontent.com/37346028/203657184-3f261d07-2456-427d-a4ee-b20b7f593a03.png)

17. Teniendo el template funcional, procedemos al autoscaling del proyecto. Iniciamos creando una imagen AMI del template con las siguientes configuraciones.

![image](https://user-images.githubusercontent.com/37346028/203660723-b1aba717-6fdb-4372-af7c-92340eb60ad1.png)

18. Creamos un target group para utilizar en el autoscaling group con las siguientes configuraciones.

![image](https://user-images.githubusercontent.com/37346028/203660905-2db8eb29-4942-428d-abce-a78c17de99ba.png)

19. Creamos un Elastic Load Balancer con las siguientes configuraciones, añadiendo como listener en HTTPS los certificados del dominio importándolos por ACM.

![image](https://user-images.githubusercontent.com/37346028/203667513-c3ccfe0b-daa4-4879-94a8-e644a948b998.png)

![image](https://user-images.githubusercontent.com/37346028/203667627-03ab498b-f3e0-4ba0-bd74-7c5ad8f059a1.png)

![image](https://user-images.githubusercontent.com/37346028/203667670-cb9302da-e94d-4796-b5d8-923a5773fcec.png)

![image](https://user-images.githubusercontent.com/37346028/203667704-085e8457-1a0a-444a-a050-e59a04fcbe0d.png)

![image](https://user-images.githubusercontent.com/37346028/203668063-6f1e2dc5-5452-468f-87f2-fe5e9cc25e0e.png)

20. Luego, creamos y configuramos un launch template, con las siguientes configuraciones.

![image](https://user-images.githubusercontent.com/37346028/203668136-b3ee0359-c11c-45c8-b927-39d2ef02458d.png)

![image](https://user-images.githubusercontent.com/37346028/203668196-a5987d27-e45e-42cd-ba49-abe93cc799ce.png)

![image](https://user-images.githubusercontent.com/37346028/203668255-44bf5f0a-cadd-4288-927c-8d767805835d.png)

21. Finalmente, creamos a partir de esa plantilla, un grupo de autoscaling, con las siguientes configuraciones, utilizando la AMI creada anteriormente y la plantilla de lanzamiento.

![image](https://user-images.githubusercontent.com/37346028/203668328-87816879-60c2-4d01-96cc-34aef4cb86bf.png)

![image](https://user-images.githubusercontent.com/37346028/203668358-e34b413c-80d4-4666-aa46-8c243b80e533.png)

![image](https://user-images.githubusercontent.com/37346028/203668393-a23fba96-1571-48b0-8fe8-0aaf49c11702.png)

![image](https://user-images.githubusercontent.com/37346028/203668469-7ae00476-4e94-4221-98d7-61fc1b7ddd03.png)

22. Al revisar las instancias, podemos identificar que el grupo de autoscaling creó las instancias configuradas.

![image](https://user-images.githubusercontent.com/37346028/203668539-12af7aed-2773-438a-ad88-06d17615fcae.png)

## Detalles técnicos
Se usó EC2 en AWS para desplegar las máquinas virtuales.  
Se usaron contenedores de Docker.  
Se usó Cerbot y Let's Encrypt para asignar un certificado SSL válido.  
Se usó EFS en AWS para hacer el servidor NFS.  
Se usó el servicio de AMI en AWS para replicar los Moodle template.  
Se usó MariaDB con el servicio RDS en AWS, para la creación de la base de datos.  
Se usó el grupo de auto scaling en AWS.  
Se usó ELB en AWS para la creación del balanceador de cargas.  

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Docker, Moodle y AWS.

# IP o nombres de dominio en nube o en la máquina servidor.
IP pública de la máquina servidor del Moodle template: 44.201.41.231  
Nombre de dominio: npenuela.tk  
Dominio con certificación ssl: https://proyecto25.npenuela.tk

## Una mini guia de como un usuario utilizaría el software o la aplicación
El usuario puede acceder desde cualquier navegador al link https://proyecto25.npenuela.tk y disfrutar de la aplicación.

## Resultados o pantallazos 
![image](https://user-images.githubusercontent.com/37346028/203670072-26f89a55-11d8-4c4c-8520-ab32f9d045a6.png)

# Referencias:
## https://github.com/st0263eafit/st0263-2022-2.git
## https://docs.google.com/document/d/1jtZBV9h_guHMZzr6ZLSDtEDUB04xUVDT/edit

#### versión README.md -> 1.0 (2022-noviembre)