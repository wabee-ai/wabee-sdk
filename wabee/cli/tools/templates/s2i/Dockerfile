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

# Install Poetry
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
RUN python -m pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry config virtualenvs.create false && \
    poetry config installer.max-workers 10

# Add poetry to PATH
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Set S2I scripts location
LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

# Copy S2I scripts
COPY ./s2i/bin/ /usr/libexec/s2i

# Set the default port for applications built using this image
EXPOSE 50051

# Set the default CMD for the image
CMD ["/usr/libexec/s2i/usage"]
