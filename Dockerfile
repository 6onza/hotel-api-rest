FROM python:3.12.0a4-alpine3.17

WORKDIR /app

COPY ./requirements.txt ./

RUN apk update \
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev openssl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]