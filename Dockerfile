FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requiremrnts.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt