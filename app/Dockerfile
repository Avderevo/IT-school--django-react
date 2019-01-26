FROM alpine:3.8
COPY .. /opt/app
COPY ../requirements.txt /opt/app/requirements.txt

RUN apk update && apk add --update --no-cache --progress \
    make \
    python3 \
    ca-certificates \
    bash bash-completion \
    && update-ca-certificates 2>/dev/null || true \
    && apk add --no-cache --virtual=.build-dependencies \
    python3-dev \
    build-base \
    supervisor \
    postgresql-dev \
    nginx \
    linux-headers \
    sqlite \
    pcre-dev \
    musl-dev \
    jpeg-dev libpng-dev freetype-dev \
    && rm -rf /var/cache/apk/*

RUN pip3 install --upgrade pip setuptools \
    && pip3 install -r /opt/app/requirements.txt

COPY ../Deploy/nginx.conf /etc/nginx/nginx.conf
COPY Deploy/nginx-site.conf /etc/nginx/conf.d/default.conf

VOLUME ["/opt/app/media"]
WORKDIR /opt/app
EXPOSE 8000
CMD ["./Deploy/start_in_docker.sh"]ker.sh"]