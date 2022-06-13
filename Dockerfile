FROM python:3.8-slim-buster

RUN apt update -y && apt upgrade -y

RUN useradd --user-group --system --create-home --no-log-init pythonuser

WORKDIR /api

RUN chown -R pythonuser:pythonuser /api \
    && chmod 755 /api

ADD requirements.txt /api

USER pythonuser

ENV WEATHER_ENDPOINT=$WEATHER_ENDPOINT

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "app.py", "-h", "0.0.0.0"]