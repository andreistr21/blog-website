# pull the official base image
FROM python:3.11-alpine

ENV SECRET_KEY=ox&1urjnp++!8vobj0k4un*474tg5g#d_k0srznzt@ixlhhino
ENV DEBUG=True
ENV ALLOWED_HOSTS=*
ENV CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8080/
ENV DATABASE_URL=postgres://postgres:7895@db:5432/blog

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app
# RUN python /code/manage.py migrate

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]