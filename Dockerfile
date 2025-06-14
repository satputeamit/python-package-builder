FROM python:3.11-slim

# Install Python 3.11 headers, build tools, and pybind11
RUN apt-get update && apt-get install -y \
    build-essential \
    python3.11-dev \
    pybind11-dev \
    && pip install pybind11

WORKDIR /build

ENTRYPOINT ["/bin/bash", "-c"]
