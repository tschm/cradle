FROM ubuntu:22.04

# Set environment for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive \
    # Prevents Python from writing pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # Ensures Python output is sent straight to terminal
    PYTHONUNBUFFERED=1 \
    # Adds user's local bin to PATH
    PATH="/home/runner/.local/bin:${PATH}"

# Install system dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    sudo \
    software-properties-common \
    build-essential \
    ca-certificates \
    gnupg \
    zip \
    unzip \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python-is-python3 \
    biber \
    # Clean up apt cache \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (more reliable method)
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update  \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g npm@latest

# Install Tectonic (LaTeX compiler)
#RUN curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh \
#    && mv ./tectonic /usr/local/bin/ \
#    && chmod +x /usr/local/bin/tectonic

# Create non-root user early for better layer caching
RUN useradd -m -u 1001 -s /bin/bash runner \
    && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to runner user for Python package installation
USER runner
WORKDIR /home/runner

# Install common Python packages
RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir \
    pytest \
    pytest-cov \
    pytest-html \
    pytest-random-order \
    jupyter-book \
    sphinx-math-dollar \
    pdoc \
    marimo \
    toml \
    requests \
    packaging \
    deptry

RUN python3 -m pip install --no-cache-dir \
    pre-commit

# Label the image
LABEL maintainer="cradle"
LABEL description="Docker image for running GitHub Actions workflows"
LABEL version="1.0"
LABEL org.opencontainers.image.source="https://github.com/tschm/cradle"

# Default command (GitHub Actions will override this)
CMD ["/bin/bash"]
