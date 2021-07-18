FROM python:3.9.6-alpine

RUN apk add --no-cache --update python3 py3-pip bash

COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -f requirements.txt

# RUN python /app/manage.py collectstatic --noinput

# CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "notesAPITest.wsgi", "--chdir=/app", ]
# CMD gunicorn --bind 0.0.0.0:$PORT notesAPITest.wsgi --chdir=/app

COPY ./start /app/
RUN chmod +x ./start

EXPOSE 8000

CMD ["./start"]

