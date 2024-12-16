FROM python:3.10-slim
WORKDIR /app
COPY . .

ENV PYTHONPATH=/app

RUN pip install -r requirements.txt
CMD ["python", "foodfacts/cli.py"]
