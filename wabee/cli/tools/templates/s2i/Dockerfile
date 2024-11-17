FROM python:3.11-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    curl \
    build-essential \
    python3-dev \
    git && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry with explicit virtualenv configuration
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

RUN python -m pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry config virtualenvs.create false --local && \
    poetry config cache-dir ${POETRY_CACHE_DIR}

# Create non-root user for runtime
RUN useradd -r -s /bin/bash -m -d /app wabee

# Set S2I scripts location
LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

# Copy S2I scripts
COPY ./s2i/bin/ /usr/libexec/s2i

# Set the default port
EXPOSE 50051

# Switch to non-root user for runtime
USER wabee
WORKDIR /app

# Set the default CMD
CMD ["/usr/libexec/s2i/usage"]
