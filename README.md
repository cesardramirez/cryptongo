## Descripción
Proyecto hecho con Python (3.5.2) y MongoDB (4.0.2)

## Instalación y ejecución
Ubuntu 16.x

    python3 -V
    wget https://bootstrap.pypa.io/get-pip.py -O ~/get-pip.py
    sudo python3 ~/get-pip.py
    sudo apt-get install python3-venv
    git clone https://github.com/cesardramirez/cryptongo.git
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Opción alternativa (paquetes recientes)

    ...
    source venv/bin/activate
    pip install --upgrade pip
    pip install pymongo
    pip install flask
    pip install requests