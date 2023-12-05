FROM python:3.10


WORKDIR /kardan


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /kardan
EXPOSE 8080


