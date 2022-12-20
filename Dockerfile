FROM python:alpine

WORKDIR /app

COPY . .

RUN pip install -r req.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]