FROM python:3.8



WORKDIR /var/pong/
COPY requirements.txt requirements.txt

RUN pip install -U -q pip
RUN pip install -q -r requirements.txt

COPY config.yml config.yml
COPY run.sh run.sh
COPY pong.py pong.py

EXPOSE 8000

CMD bash /var/pong/run.sh