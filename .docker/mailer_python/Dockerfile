# Define a minimal docker container
FROM python:3.7.1-alpine3.7

#requirements installation
RUN apk update && apk add  --no-cache --update  gcc python3-dev\
                                                py3-pip\
                                                musl-dev\
                                                bash
# Define production|development environment variable
ENV ENVIRONMENT production

# Prevent stdout to be buffered
ENV PYTHONUNBUFFERED 1

# Exporse a specific port
ENV PORT 8000

# Expose the number of workers based on CPU
ENV WORKERS 1

# Expose the type of worker class
ENV WORKERCLASS sync

RUN mkdir -p /opt/mailer_python
WORKDIR /opt/mailer_python
ADD ./mailer_python /opt/mailer_python
RUN pip3 install -r requirements.txt
EXPOSE ${PORT}
CMD ["python3", "manage.py"]