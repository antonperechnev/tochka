FROM python:3.7

RUN pip install -r opt/tochka/Docker/Python/modules.txt

EXPOSE 8000
WORKDIR /opt/tochka/app
ENV POSTGRES_USER="postgres" POSTGRES_PASSWORD="tochkatest" POSTGRES_HOST=postgres POSTGRES_PORT=5432
POSTGRES_DB="tochka"