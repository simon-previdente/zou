FROM python:3.8.5

RUN apt-get update && apt-get install -y \
	ffmpeg \
	postgresql-client \
	lsof \
	net-tools \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt setup.cfg setup.py /build_zou/
COPY zou /build_zou/zou/
RUN cd /build_zou/ && pip install -r requirements.txt && python setup.py build && python setup.py install
RUN pip install allure-pytest

RUN mkdir -p /opt/zou/previews /opt/zou/zou /etc/zou /var/log/zou
COPY docker-files/init_zou.sh /usr/local/bin/init_zou.sh
COPY docker-files/gunicorn-events.conf.py docker-files/gunicorn.conf.py /etc/zou/
RUN chmod 755 /usr/local/bin/init_zou.sh
