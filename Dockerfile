FROM python:3.12-slim

# Install dependencies for git and building packages
# RUN apk add -y --no-cache build-base
# RUN  apk update && apk add git

RUN apt-get update && apt-get install -y git

RUN groupadd repos && useradd -ms /bin/bash spongebob
ENV HOME=/home/spongebob

# Create the /repos directory (if it doesn't exist)
RUN mkdir -p /repos \
&& chown -R spongebob:repos /repos

RUN mkdir -p /db \
&& chown -R spongebob:repos /db


# Install uv globally
RUN pip install uv

WORKDIR $HOME/app

# Copy project files
COPY pyproject.toml .
COPY uv.lock* .

# Create virtualenv manually and use uv to install deps
RUN python -m venv .venv \
    && .venv/bin/pip install --upgrade pip setuptools wheel \
    && .venv/bin/pip install uv \
    && .venv/bin/uv sync

COPY . .
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Switch to the spongebob user
USER spongebob


ENV IN_CONTAINER=1


ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8888
# Use venv's uvicorn to run app
CMD [".venv/bin/python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
