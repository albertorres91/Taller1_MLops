FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt 

WORKDIR /model/app

EXPOSE 5000

CMD ["python", "app.py"]
