FROM python:3.11

ARG PROXY
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG FALSE
ENV LOG_FILE app.log

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends supervisor

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
