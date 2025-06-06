FROM python:3.11.8-slim-bookworm
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev --no-install-recommends

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./app /app
ENTRYPOINT [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]