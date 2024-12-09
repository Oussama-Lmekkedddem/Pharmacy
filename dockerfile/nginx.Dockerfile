FROM nginx:latest

USER root

RUN apt update && \
    apt install -y nano apt-utils certbot python3-certbot-nginx

COPY config/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
