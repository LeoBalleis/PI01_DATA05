FROM tiangolo/uvicorn-gunicorn-fastapi

RUN pip install pandas

EXPOSE  8080

COPY ./app /app 



