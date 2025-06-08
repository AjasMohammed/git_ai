# ---------- Stage 1: Build stage ----------
FROM python:3.12-slim AS builder


# Install dependencies for git and building packages
RUN apt-get update \
    && apt-get install -y libpq-dev gcc python3-dev \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/man /usr/share/doc

WORKDIR /app

# Install uv globally
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY uv.lock* .

# Create virtualenv manually and use uv to install deps
RUN python -m venv .venv \
    && .venv/bin/pip install --upgrade pip setuptools wheel \
    && .venv/bin/pip install uv \
    && .venv/bin/uv sync

# ---------- Stage 2: Final minimal image ----------
FROM python:3.12-slim

# Install git
RUN apt-get update && apt-get install -y git libpq5 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create the /repos directory (if it doesn't exist)
RUN groupadd repos && useradd -ms /bin/bash -g repos spongebob \
    && mkdir -p /repos /db \
    && chown -R spongebob:repos /repos /db

ENV HOME=/home/spongebob

WORKDIR $HOME/app
# Copy only the venv from builder stage
COPY --from=builder /app/.venv .venv

COPY . .
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Clean up python cache
RUN find .venv -type d -name "__pycache__" -exec rm -r {} + \
    && find .venv -type f -name "*.pyc" -delete

# Switch to the spongebob user
USER spongebob


ENV IN_CONTAINER=1


ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8888
# Use venv's uvicorn to run app
CMD [".venv/bin/python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
