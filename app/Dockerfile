FROM python:3.10.4

WORKDIR /app

COPY requirements.txt .

ENV PYTHONPATH=/app

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
