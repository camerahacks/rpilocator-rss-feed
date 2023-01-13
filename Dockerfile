FROM python:3-alpine

WORKDIR /usr/src/app

COPY ./rpilocator-rss-global.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "./rpilocator-rss-global.py"]