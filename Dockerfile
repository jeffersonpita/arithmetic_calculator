FROM --platform=linux/amd64 python:3.9-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /arithmetic_calculator_api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:80
