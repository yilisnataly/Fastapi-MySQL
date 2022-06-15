FROM python:3.9

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt


RUN pip install -r /app/requirements.txt

COPY ./ /app

EXPOSE 8081

ENV PYTHONUNBUFFERED 1

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=5 \
    CMD curl -s --fail http://localhost:8081/health || exit 1

CMD [ "uvicorn", "app:app", "--reload", "--host=0.0.0.0" ]