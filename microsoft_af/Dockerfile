# Using Ubuntu 24.04
# Base image
FROM ubuntu:24.04 AS base-image

# Avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
      && apt-get install -y tzdata software-properties-common \
      && add-apt-repository ppa:deadsnakes/ppa \
      && apt-get install --no-install-recommends -y \
      python3.12 \
      python3.12-venv
      
# Builder image
FROM base-image AS python-builder-image

# Install Python 3.12 and build tools
RUN apt-get install -y \
      python3.12-dev \
      python3-pip \
      python3-wheel \
      build-essential \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*/*

# Create and activate virtual environment
# Using final folder name to avoid path issues with packages
RUN python3.12 -m venv /home/agent-smith/venv
ENV PATH="/home/agent-smith/venv/bin:$PATH"

# Install requirements
COPY microsoft_af/requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Runner image
FROM base-image AS runner-image

# Run the script
ENTRYPOINT [ "devui", "--host", "127.0.0.1", "--port", "8081"]

RUN apt-get install -y \
      curl \
      groff \
      jq \
      less \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home agent-smith
COPY --from=python-builder-image /home/agent-smith/venv /home/agent-smith/venv

# Switch to non-root user, create app directory, and set as working directory
USER agent-smith
RUN mkdir /home/agent-smith/code
WORKDIR /home/agent-smith/code

# Copy app files
COPY microsoft_af/joker_agent ./joker_agent

# activate virtual environment
ENV VIRTUAL_ENV=/home/agent-smith/venv \
      PATH="/home/agent-smith/venv/bin:$PATH"