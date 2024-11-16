FROM python:3.11-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Set S2I scripts location
LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

# Copy S2I scripts
COPY ./s2i/bin/ /usr/libexec/s2i

# Set the default port for applications built using this image
EXPOSE 50051

# Set the default CMD for the image
CMD ["/usr/libexec/s2i/usage"]
