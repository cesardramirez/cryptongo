ENV=$(env)

# Obtiene las imagenes iniciales
get-images:
	docker pull mongo:4.0

# Crea la red para la comunicacion entre contenedores
create-network:
	docker network create cryptongo

# Crea e inicia los contenedores por medio del docker-compose.yml
start-development:
	docker-compose up -d

# Carga la data de la BD de Mongo en su contenedor
load-mongo:
	# load mongo data
	docker exec -it crypto-mongodb bash -c 'mongorestore /backup_bd/backup-2018-10-04'

# Detiene todos los contenedores
stop-development:
	docker-compose stop