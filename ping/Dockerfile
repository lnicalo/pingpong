FROM python:3.8



WORKDIR /var/ping/
COPY requirements.txt requirements.txt

RUN pip install -U -q pip
RUN pip install -q -r requirements.txt

COPY config.yml config.yml
COPY run.sh run.sh
COPY ping.py ping.py
COPY test_ping.py test_ping.py

EXPOSE 8000

CMD bash /var/ping/run.sh