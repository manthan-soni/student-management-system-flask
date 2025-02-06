FROM python:3.8.10

WORKDIR /flask-app

COPY requirements.txt .

RUN  pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3", "server.py"]
