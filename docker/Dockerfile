FROM ubuntu:22.04

# Set non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
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
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Verify Node.js installation
RUN node --version && npm --version

# Install additional tools that might be needed for GitHub Actions
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    biber \
    && rm -rf /var/lib/apt/lists/*

# Install Tectonic (LaTeX compiler)
RUN curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh \
    && mv ./tectonic /usr/local/bin/ \
    && chmod +x /usr/local/bin/tectonic

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
    pandas

# Create a non-root user for running actions
RUN useradd -m -s /bin/bash runner \
    && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set working directory
WORKDIR /home/runner

# Switch to the runner user
USER runner

# Set environment variables
ENV HOME=/home/runner
ENV PATH=$HOME/.local/bin:$PATH

# Label the image
LABEL maintainer="cradle"
LABEL description="Docker image for running GitHub Actions workflows with act"
LABEL version="1.0"
LABEL org.opencontainers.image.source="https://github.com/tschm/cradle"

CMD ["/bin/bash"]
