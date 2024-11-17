FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    curl \
    build-essential \
    python3-dev \
    git && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user for runtime
RUN useradd -r -s /bin/bash -m -d /app wabee

# Create directory for pip installations and set ownership
RUN mkdir -p /app/.local && \
    chown -R wabee:wabee /app/.local

# Set environment variable for pip to install packages in user directory
ENV PATH=/app/.local/bin:$PATH \
    PYTHONPATH=/app/.local/lib/python3.11/site-packages:$PYTHONPATH \
    HOME=/app

# Set S2I scripts location
LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

# Copy S2I scripts
COPY ./s2i/bin/ /usr/libexec/s2i

EXPOSE 50051

USER wabee
WORKDIR /app

CMD ["/usr/libexec/s2i/usage"]
