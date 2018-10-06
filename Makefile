ENV=$(env)

# Obtiene las imagenes iniciales
get-images:
	docker pull mongo:4.0

# Crea la red para la comunicacion entre contenedores
create-network:
	docker network create cryptongo

# Construir las imagenes a partir del Dockerfile
build-development:
	docker build -t "agent-dev" .

# Crea e inicia los contenedores por medio del docker-compose.yml
#  Si se hace cambios en el arhivo yml, recrea y vuelve a crear el contenedor.
start-development:
	docker-compose up -d

# Carga la data de la BD de Mongo en su contenedor
load-mongo:
	# load mongo data
	docker exec -it crypto-mongodb-dev bash -c 'mongorestore /backup_bd/backup-2018-10-04'

# Elimina de manera local los archivos fisicos de la BD
clean-mongo:
	sudo rm -r ~/mongo_db

# Detiene todos los contenedores
stop-development:
	docker-compose stop