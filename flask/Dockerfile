FROM python:3.7

COPY . /app
WORKDIR /app
ADD docker-compose.yml /docker-compose.yml
ADD node-play.yml /node-play.yml
ADD test_hdg.pem /test_hdg.pem
ADD hosts /hosts


RUN pip3 install -r requirement.txt

CMD ["python3", "./app.py"]
#CMD ["uwsgi", "uwsgi.ini"]
