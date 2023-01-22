FROM python:3.11

RUN apt-get update \
  && apt-get install -y cron

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#

COPY cron.py ./

RUN ["python", "./cron.py"]

RUN crontab -l | { cat; echo "0 12 * * * python cron.py"; } | crontab -
