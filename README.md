It is created while I studying the docker 
	############################################################################################################################
 Reference
	#	https://docs.docker.com/reference/cli/docker/  : basic commands 															
	#	Docker Hub Container Image Library | App Containerization: docker hub (The image directory you can think)					
	#	https://docs.digitalocean.com/products/droplets/how-to/add-ssh-keys/to-existing-droplet/  : add the key to existing droplet	
	#	*The directory to store the public key is "~/.ssh/authorized_keys"														
	#	https://docs.digitalocean.com/products/droplets/how-to/add-ssh-keys/create-with-putty/ : create key with putty				
	#	https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/putty/ : connect with putty					
	############################################################################################################################
		
Links: 
	vagrant cloud : https://app.vagrantup.com/boxes/search
	installation docs: https://docs.docker.com/ , https://docs.docker.com/engine/install/ubuntu/
	
	* docker hub (where we can get docker images, we ca upload our own docker images here also) : https://hub.docker.com/
	* docker hub is the registry for docker images . docker image can be consider as archived continer and the container can be created from it.
	

Some Linux Commands to remember:
	ps -ef  : display information about running processes
	du -sh <dir/file/other>: checking disk usage
	id <usernam (eg: root, vagrant)> : show the details og the user loke group_id, guoup_name, etc..
	cat /etc/os-release  ---> get the OS details 
	
	

########################
########DOCKER##########
########################

* switch to root user. If we do not switch to root user a permission denied error will occure while running any docker commands. ie bcz by default the docker daemon can connect by root user through CLI. if we want any other user want to run the docker command, then we have to add the user in todocker group. it can be done either by edit the /etc/goup file (add the user in the group) , or bu using "sudo usermod -aG docker <user_name>".


To validate our docker installed succefully : run the command  "docker run hello-world" :-> what it does that create container from the image hello-world,the image hello-world will be present in the docker hub

docker run hello-world -> what it does that create container from the image hello-world, the image hello-world will be present in the docker hub


*docker ps -----------------------------> show the active contaners
*docker ps -a --------------------------> show all the container including the dead one
systemctl status docker ---------------> get status of docker
docker images -------------------------> list all the images in the local m/c
docker pull nginx ---------------------> it will pull the nginx image from dockerhub by default
docker stop <container_id or name> ----> stop the docker
docker rm <container_id or name>  -----> remove the docker
docker start <container_id or name> ---> start the docker
docker rmi <image_name> ---------------> remove the image
docker exec -it <container_id or name> /bin/bash --------> to execute commands on a container (while executing this command we wil inside the container)
decker inspect <container_id or name> -> detail of container and image in a JSON format
docker logs <container_id> ------------> it is helpfull when something went wrong

docker run -d --name <name_of_the_docker_we_needed> -p 9080:80 <name_of_the_image>:<tag>  -> General way to run the docker. Eventhough check in the dockerhub for a particular image how to run


Note : port mapping
       ------------
		example to run an nginx image : "docker run --name some-nginx -d -p 8080:80 some-content-nginx" -->8080 port in the host m/c mapped with port 80 in the container
		1."-d" in docker commands tell that run in detatched mode, ie continuously run in background
		2."-p 8080:80" : This option maps a port on your host machine (local computer) to a port inside the container.
		In this case, it maps port 8080 on your host machine to port 80 inside the container. This allows you to access the web server running 
		within the container by visiting http://localhost:8080 in your web browser.

Note: 
	A container running on top of a directry, which will mimic as an OS but actually it is not an OS (We can think it like this).
	"/var/lib/docker" -> It serves as the default storage location for Docker on your machine, holding essential data related
						 to your container images, containers, and named volumes 
	"/var/lib/docker/containers" -> This subdirectory stores data specific to running and stopped Docker containers.
	
Note: We generally login to a VM by ssh connection, But since the container is a process, so we cannot login to a process using ssh. 
	  The docker exec command allows you to execute a new command within a running Docker container. This provides a way to interact with 
	  the container's file system, run programs, or troubleshoot issues directly from your terminal. 
	  
	  command will be: docker exec <docker_id or name> <command_to_execute>
	  
	  When you use the -it option with docker exec, it allocates a pseudo-TTY. This creates a virtual terminal environment within your
	  existing terminal window. ie we can interact with the container after the command 
	  " docker exec -it <docker_id or name> /bin/bash " -> on execcuting this, we will be inside the container (get in to the container)
	  some container wont have /bash so instead of use /sh (check the /bin directory if anything happen wrong)
	  
	  

Note: Volume (To preserve the data of docker in the host machine) 
	--------------------------------------------------------------
 --	1. Docker containers are ephemeral, meaning they are designed to be lightweight and disposable. By default, any data created or modified within a
	container is lost when the container stops or is deleted.
	Volumes provide a way to store data outside of the container's writable layer, ensuring that the data persists even after container restarts or
	upgrades. This allows you to manage your application's data independently of the container's lifecycle.
	
	* to get the details of an image like what port it running , what is the volume directory , etc 
	    docker pull <image>:<tag>
		docker inspect <image>:<tag>
	  Now we will get a JSON and go through it.
	
	it is managed by : "/var/lib/docker/volumes/" directory on linux. the files that need to be persistent after the deletion or updation of container
	will store in this file on the *host machine*. 
	
	run: "docker volume" -> which give the all commands existing

 --	2. Another method is "Bind mounts" : (It usually use to inject the data to the container from host machine)
						  -----------
	   * which is store anywhere in the host system, This may change execute the "docker inspect <image_name>:<tag>" ,and look in the volume field in the json
	   * Here we can map any directory in the host machine to a container directory
	   * This will do when we need to change the container data, we can do it from the host machine directory . The changes done in the host directory
	     will be reflect on the container directory
	   * eg:- case-1 :  while run the image by docker ,  we have to pass it an argument from CLI
	               ie, "docker run --name <name_needed_for_the_container> -e <environment_variable_if_any> -p 9000:8000 -v <directory_in_host>:<directory_in_container>"     
	   
	   * eg:- case-2 : we can configure it in the compose file: 
	               ie, in the compose.yml file , add the mapping under the title 'volume', below is an example
				 
				      services:
						  fastapi:
							build:
							  context: .
							  target: builder
							container_name: fastapi-application
							environment:
							  PORT: 8000
							ports:
							  - '9000:8000'
							volumes:
							  - /root/nashith_practice/5.proj_with_db/mount_file_dir:/var/lib/test  # here is the injecting "from host to docker"
							restart: "no"
				   
	

	
============================================================================================================================

###############################################
############DOCKER IMAGE BUILDING##############	  
###############################################

***We are creating a file named as "Dockerfile"(name in this mandatory I think) and building an image from it by "docker build" command***

NB: When we writind a Dockerfile it should be non interactive, otherwise it will fail the build. So to make the file non interactive 
    we introduce a variable DEBIAN_FRONTEND as set it as noninteractive --> ENV DEBIAN_FRONTEND=noninteractive
	
	
####Build docker image####
--------------------------	
docker build -t <image_name>:<tag> <file_path_whr_Dockerfile_exist7> ---------->To Build image fom the Dockerfile  

eg: docker build -t my_img:v1 . --> build image from current directory (. is bcz Dockerfile is present in the current file)



*********************************************************************************************************
=====To host our created image in docker hub ===== NB: to push the image , the image name should be ib the format of "<account_name>/<image_name>".
														so while building the image gave name in this format.
1. create an account in the dockerhub,  we can make it as public or private our image
2. login from docker : execute "docker login" command in CLI
3. give username and password while asking
4. push the image taht we created : execute "docker push <image_name>:<tag>"
5. stop

*************************************************************************************************************
Dockerfile Instructions:

* FROM -------> Base Image
* LABELS -----> Adds meta data to image
* RUN --------> execute commands in a new layer and commit the results
* ADD/COPY ---> Adds files and folder into image
* CMD --------> Runs binaries/commands on docker run
* ENTRYPOINT -> Allows you to configure a container that will run as an executable
* VOLUME -----> Creates a mount point and marks it as holding externally mounted volumes
* EXPOSE -----> Container listens on the specified network ports at runtime
* ENV --------> Sets the environment variable
* USER -------> Sets the username (or UID)
* WORKDIR ----> Stes the working directory
* ARG --------> Defines a variable that a usr can pass at build-time
* ONBUILD ----> Adds to the image a trigger instruction to be executed at a later time


Ref: https://docs.docker.com/reference/dockerfile/

eg:-Dockerfile
--------------
FROM ubuntu:latest
LABEL "Author"="Nashith"
LABEL "Projest"="Demo"
ENV DEBIAN_FRONTEND=nonintractive
RUN apt update && apt install git apache2 -y
RUN apt install apache2
CMD ["usr/sbinapache2ctl", "-D", "FOREGROUND"]
EXPOSE 80
WORKDIR /var/www/html
VOLUME /var/log/apache2
ADD nano.tar.gz /var/www/html


Note:  CMD and ENTRYPOINT 
	   -----------------
	   * format of this command is : CMD ["<command>", "<arguments>"]
	     eg: CMD ["echo", "hello"]
		 
	   * In the case of Entrypoint the command is : ENTRYPOINT [<"command">]
	     NB: The arguments should pass from the CLI or we have to set it by CMD
		 case1: Argument pass from CLI
			eg: ENTRYPOINT ["echo"]  -> instruction in the Dockerfile
			    after buildong the imange(let us say our image name is abc_img:v1_tag), the run command will be :--> docker run abc_img:v1_tag hello.
				
		 case2: using CMD and ENTRYPOINT
		  Assume we have following Dockerfile
		    FROM ubuntu:latest
			ENTRYPOINT ["echo"]
			CMD ["hello"]
			
			We have Two purpose for this:
			 1. ENTRYPOINT have the command and CMD have the argument(default argument for the ENTRYPOINT )
			 2. we can give some script on entrypoint that need to execute first will give in the ENTRYPOINT, then the actual command give in CMD
			    NB: priority(ENTRYPOINT) > priority(CMD)
				
	 
	 

	 
*************************************************************************************************************


###############################################
###############DOCKER  COMPOSE#################
###############################################

 * In short we can say that Docker compose is a tool to run multi containers together *
 * We can compare the docker compose to Vagrant in such a wa that 
     vagrant is for -------------> VMs
	 docker compose is for ------> Containers
 * We have a docker-compose.yml (or compose.yml) file for it: There we config the what all services we need 
 * go to the documentation for how we do it : https://docs.docker.com/compose/gettingstarted/
 * 
 

decker compose --help -> will show all the available commands
docker compose up ----> to  create and start all the services from your configuration file (compose.yml file)
docker compose up -d  ----> to  create and start all the services from your configuration file (compose.yml file), in detatched mode
docker compose down---> to remove the containers
decker cmopose ps -a --> show all the containers
docker-compose --env-file .my-env up --> create the container with specific .env file


example of compose.yml
----------------------

services:
  web:  # service 1
    build: .  # build the Dockerfile existed in the current directory(bcz of . is there)
    ports:
      - "8000:5000"  # port mapping (8000 port in the host machine is mapped to 5000 port in the container)
    develop:
      watch:
        - action: sync
          path: .
          target: /code
	volume:
		- /root/validation_studio_cloud/ValidationStudioCloud/${driver_path}:${driver_path}  # here we are using the bind mount
		- /root/validation_studio_cloud/ValidationStudioCloud/${data_transfrom_path}:${data_transfrom_path}
		
  redis:   # service 2
    image: "redis:alpine"  # name of the image, it will download the image from dockerhub 
	
	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%		
	
	
########################################################
#####################Containerisation###################
########################################################

STEPS TO SETUP OUR STACK SERVICES
1. Find the right base image from dockerhub
2. Write Dockerfile to customize Images
3. write compose.yml file to run multi containers


* Deployment via images
* 

Code Changes Affecting Container Functionality: If your code changes directly impact the functionality of your application running in the container,
you'll need to rebuild the image to incorporate those changes. This typically involves: Modifying the source code within your project directory.
Running "docker compose build" (or docker build if not using Compose) -----> to rebuild the image with the updated code.
Running "docker compose up -d" (or docker run -d) ------------------------->to restart the container(s) with the new image.

or simply run : "docker-compose up -d --build"

Note : - Every files shhould be copied to the working directory of the container that we setup
	   - 
      


#####################################################
####################Project Research#################
#####################################################

* Base image recommended for fastapi: https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
* Note: Make sure that mongodb is up before fastapi.
* Since we are using the cloud for DB, a seperate container for DB is not needed. for time being



###################################################
#############Digital Ocean MongoDB#################
###################################################

doadmin password to connect the digitalocean mongoDB: O85q437nRt9MSm26
connection string to doadmin: mongodb+srv://doadmin:O85q437nRt9MSm26@vs-mongodb-001-c4099f9a.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=vs-mongodb-001

