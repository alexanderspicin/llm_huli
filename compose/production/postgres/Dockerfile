FROM docker.io/postgres:16

# Устанавливаем необходимые зависимости для компиляции pgvector
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-all

# Клонируем репозиторий pgvector и устанавливаем расширение
RUN git clone https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install

# Копируем скрипты обслуживания
COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
