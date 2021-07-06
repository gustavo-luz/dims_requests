FROM python:3.6.12-alpine3.12

COPY . .

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev

RUN pip install -r requirements.txt

RUN crontab crontab

CMD ["crond", "-f"]

