FROM python:3.12.0a4-alpine3.17

RUN apk update 
RUN apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev openssl-dev 

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
