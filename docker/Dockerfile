FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/runner/.local/bin:${PATH}"

# Install system dependencies in a single layer with cleanup
RUN apt-get update && apt-get install -y --no-install-recommends \
    #ca-certificates \
    curl \
    #wget \
    #git \
    #sudo \
    #software-properties-common \
    #build-essential \
    #gnupg \
    #zip \
    #unzip \
    #jq \
    #python3 \
    #python3-pip \
    #python3-venv \
    #python3-dev \
    #python-is-python3 \
    #biber \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 using NodeSource recommended method
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with fixed UID for consistency
RUN useradd -m -u 1001 -s /bin/bash runner \
    && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to runner user for subsequent operations
USER runner
WORKDIR /home/runner

# Copy requirements file first for better caching
COPY --chown=runner:runner docker/requirements.txt .

# Install Python packages using recommended method
#RUN python3 -m pip install --no-cache-dir --upgrade pip \
#    && python3 -m pip install --no-cache-dir -r requirements.txt

# Label the image
LABEL maintainer="cradle" \
      description="Docker image for running GitHub Actions workflows" \
      version="1.0" \
      org.opencontainers.image.source="https://github.com/tschm/cradle"

# Default command
CMD ["/bin/bash"]
