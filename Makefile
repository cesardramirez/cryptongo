ENV=$(env)

# Obtiene las imagenes iniciales
get-images:
	docker pull mongo:4.0

# Red
create-network:
	docker network create cryptongo

start-development:
	docker-compose up -d

# Carga la data en la BD de Mongo
load-mongo:
	# load mongo data
	docker exec -it crypto-mongodb bash -c 'mongorestore /backup_bd/backup-2018-10-04'

stop-development:
	docker-compose stop