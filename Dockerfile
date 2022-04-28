FROM python:3.9.5
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./geocalc /code/geocalc

CMD ["python", "-m", "geocalc"]