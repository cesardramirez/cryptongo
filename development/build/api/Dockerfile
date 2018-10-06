FROM debian:9.3
LABEL author=cesardavid89@gmail.com
LABEL version="1.0"

RUN apt-get update
RUN apt-get -y install python3 python3-dev
RUN apt-get -y install openssh-server

COPY get-pip.py /get-pip.py
RUN python3 get-pip.py
RUN rm -f get-pip.py

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm -f /tmp/requirements.txt

# Cambiar la configuracion de ASCII por UTF-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Genera la configuracion para el ingreso al contenedor por SSH.
RUN mkdir /var/run/sshd
COPY entry.tar.gz /entry.tar.gz
RUN tar xzf entry.tar.gz
RUN rm -f entry.tar.gz
RUN chmod 0777 /entry.sh
RUN chmod +x /entry.sh
RUN mkdir /root/.ssh/

EXPOSE 22
ENTRYPOINT ["/entry.sh"]
CMD ["/usr/sbin/sshd", "-D", "-f", "/etc/ssh/sshd_config"]

WORKDIR /opt/app