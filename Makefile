ENV=$(env)

# Obtiene las imagenes iniciales
get-images:
	docker pull mongo:4.0

# Crea la red para la comunicacion entre contenedores
create-network:
	docker network create cryptongo

# Construir las imagenes a partir del Dockerfile
build-development:
	# agent
	cp requirements.txt development/build/agent/requirements.txt
	cd development/build/agent/ && docker build -t "agent-dev" .
	rm -f development/build/agent/requirements.txt

	# api
	cp requirements.txt development/build/api/requirements.txt
	cd development/build/api/ && docker build -t "api-dev" .
	rm -f development/build/api/requirements.txt

# Crea e inicia los contenedores por medio del docker-compose.yml
#  Si se hace cambios en el arhivo yml, recrea y vuelve a crear el contenedor.
#  Si se comenta la linea de command, indica que se ejecutara el servicio por medio de Pycharm por SSH.
start-development:
	cd development && docker-compose up -d

# Carga la data de la BD de Mongo en su contenedor
load-mongo:
	# load mongo data
	docker exec -it crypto-mongodb-dev bash -c 'mongorestore /backup_bd/backup-2018-10-04'

# Elimina de manera local los archivos fisicos de la BD
clean-mongo:
	sudo rm -r ~/mongo_db

# Detiene todos los contenedores
stop-development:
	cd development && docker-compose stop

api-logs-1:
	cd development && docker-compose logs api

api-logs-2:
	docker logs -f crypto-api-dev