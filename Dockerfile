FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ./

ARG DEBUG=n
ENV DEBUG=$DEBUG

ENTRYPOINT ["python", "main.py"]