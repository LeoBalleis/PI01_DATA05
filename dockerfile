FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN pip install pandas

EXPOSE  80

COPY ./app /app



