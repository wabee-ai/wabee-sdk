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

# Create non-root user for Poetry
RUN useradd -m -s /bin/bash poetry_user && \
    mkdir -p /home/poetry_user/.config && \
    chown -R poetry_user:poetry_user /home/poetry_user

# Install Poetry and configure
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_CONFIG_DIR=/home/poetry_user/.config

# Install and configure Poetry as poetry_user
RUN python -m pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    mkdir -p ${POETRY_HOME} && \
    chown -R poetry_user:poetry_user ${POETRY_HOME} && \
    su poetry_user -c "poetry config virtualenvs.create false" && \
    su poetry_user -c "poetry config installer.max-workers 10"

# Add poetry to PATH
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Set the working directory and permissions
RUN mkdir -p /tmp/src && \
    chown -R poetry_user:poetry_user /tmp/src

# Set S2I scripts location
LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

# Copy S2I scripts
COPY ./s2i/bin/ /usr/libexec/s2i

# Set the default port for applications built using this image
EXPOSE 50051

# Set the default CMD for the image
CMD ["/usr/libexec/s2i/usage"]
