FROM python:3.11-alpine

ARG PROXY
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG FALSE
ENV LOG_FILE app.log

MAINTAINER PavelCode5426

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

COPY entrypoint.sh entrypoint.sh
COPY cron /etc/cron.d/process_message
RUN chmod +x entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]