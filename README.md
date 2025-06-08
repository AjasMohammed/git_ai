# Git AI Commit Message Generator

A FastAPI app that automatically generates Git commit messages from git diffs using a Large Language Model (LLM) such as Google Generative AI. The app provides a simple UI built with FastAPI templates for easy interaction.

---

## Features

-   Automatically generate commit messages from git diffs.
-   Uses Python Git module to generate diffs automatically.
-   Integrates LangChain with prompt templates to create meaningful commit messages.
-   Simple UI for inputting repository name and path.
-   Supports running directly on the system or inside Docker.
-   Uses SQLite by default or PostgreSQL when configured via Docker Compose.
-   Dependency management with [`uv`](https://docs.astral.sh/uv/) package manager.

---

## How It Works

1. User provides the repository name and local path (or mounts the repo in Docker, the volumes should be mounted in the /repos/ directory).
2. The app generates git diffs using the Python Git module.
3. Diffs are passed to an LLM with a LangChain prompt template.
4. The LLM generates a commit message based on the diffs.
5. The generated commit message is displayed in the UI.

---

## Getting Started

### Prerequisites

-   Python 3.12+
-   Docker (optional, for containerized deployment)
-   LLM API key for the AI service (e.g., Google Generative AI)

### Environment Variables

| Variable            | Description                               | Required For        |
| ------------------- | ----------------------------------------- | ------------------- |
| `LLM_API_KEY`       | API key for accessing the LLM model       | All modes           |
| `DATABASE_URL`      | Database connection URL (Postgres/SQLite) | local mode (optional)           |
| `POSTGRES_USER`     | Postgres username                         | Docker Compose mode |
| `POSTGRES_PASSWORD` | Postgres password                         | Docker Compose mode |
| `POSTGRES_DB`       | Postgres database name                    | Docker Compose mode |
| `DB_PORT`           | Postgres port                             | Docker Compose mode |

---

## Running the App

### Running Locally (without Docker)

1. Clone the repo and install dependencies using [`uv`]((https://docs.astral.sh/uv/)):
    - activate the virtual environment, using uv or any other method of your choice
    ```bash
    pip install uv  # install the uv package manager
    ```

    ```bash
    uv sync  # install dependencies
    ```

2. Run the app:

    ```bash
    uvicorn main:app --reload
    ```

### Running Locally (with Docker)

1. Build the Docker image:

    ```bash
    docker build -t git-ai .
    ```

2. Run the Docker container:

    ```bash
    docker run -d -p 8888:8888 --name git-ai \
    -e LLM_API_KEY="YOUR_LLM_API_KEY" \
    -e DATABASE_URL="postgresql://postgres:postgres@localhost:5432/git-ai" \
    -v "path/to/repo":/repos/"repo_name" \  # replace with your local repo path
     git-ai
    ```

    multiple paths can be added like this: `-v "path/to/repo1":/repos/"repo_name1" -v "path/to/repo2":/repos/"repo_name2"`

3. Access the app at http://localhost:8888

---

## Docker Compose

1. Create a `.env` file with the required environment variables.
2. Add repo paths to the `volumes` section of the `docker-compose.yml` file.

    ```yaml
    app:
        volumes:
            - /path/to/repo1:/repos/repo_name1
            - /path/to/repo2:/repos/repo_name2
    ```

3. Run Docker Compose:

    ```bash
    docker compose up -d
    ```

4. Access the app at http://localhost:8888

---

### Notes

-   When running in Docker, always mount your local repos under /repos or update the path accordingly.

-   The app automatically detects repo names from folder names when running inside Docker.

-   SQLite is the default database if Postgres is not configured.

---
