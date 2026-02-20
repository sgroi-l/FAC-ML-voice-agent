# Start from a Python 3.13 base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install uv (Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first (Docker caches this layer if they don't change)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy the rest of the application code
COPY . .

# Run the agent
CMD ["uv", "run", "agent.py", "start"]
