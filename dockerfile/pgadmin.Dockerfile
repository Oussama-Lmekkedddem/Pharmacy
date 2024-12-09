FROM dpage/pgadmin4:latest

USER root

RUN apk update && \
    apk add nano

COPY config/pgadmin.conf /pgadmin4/config_local.py

EXPOSE 80

CMD ["python3", "/pgadmin4/web/pgAdmin4.py"]
