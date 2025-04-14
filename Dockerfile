FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /app/logs

EXPOSE 5000 

CMD ["python3", "app.py"]