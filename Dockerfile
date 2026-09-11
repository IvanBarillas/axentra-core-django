FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Usuario de aplicacion sin privilegios. No se asume UID/GID root en runtime,
# lo que mantiene la imagen compatible con contenedores rootless (Podman).
RUN groupadd --gid 1000 axentra \
    && useradd --uid 1000 --gid axentra --create-home --shell /usr/sbin/nologin axentra

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .

# El build no depende de un archivo .env.build. Los valores seguros por
# defecto y RepositoryEmpty permiten recolectar los estaticos.
RUN DJANGO_ENV=build DJANGO_SETTINGS_MODULE=core.settings.development \
    uv run python manage.py collectstatic --noinput

# Directorios de escritura en tiempo de ejecucion, propiedad del usuario
# de aplicacion (staticfiles/media ya existen tras collectstatic; logs y
# sent_emails los crean los settings de cada entorno si no existen).
RUN mkdir -p /app/staticfiles /app/media /app/logs /app/sent_emails \
    && chown -R axentra:axentra /app

USER axentra

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
