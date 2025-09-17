FROM python:3.10-slim-bullseye   

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]   # change to your entrypoint file
