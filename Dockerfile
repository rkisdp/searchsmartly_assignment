FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000
