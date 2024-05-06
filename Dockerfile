FROM python:3.8.10

WORKDIR /flask-app

COPY requirement.txt .

RUN  pip3 install -r requirement.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3", "server.py"]
