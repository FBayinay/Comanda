FROM python:3.12.5-slim

ENV GECKODRIVER_VER=v0.31.0
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.local/bin

RUN useradd --create-home --home-dir /home/flaskapp flaskapp

WORKDIR /home/flaskapp

USER flaskapp
RUN mkdir app

COPY ./app ./app
COPY ./app.py .

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]