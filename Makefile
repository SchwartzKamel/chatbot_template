# Variables
ADK_DOCKERFILE ?= google_adk/Dockerfile
ADK_COMPOSEFILE ?= google_adk/docker-compose.yml
ADK_IMAGE_NAME ?= adk-chatbot-template
ADK_TAG ?= latest

MAF_DOCKERFILE ?= microsoft_af/Dockerfile
MAF_COMPOSEFILE ?= microsoft_af/docker-compose.yml
MAF_IMAGE_NAME ?= maf-chatbot-template
MAF_TAG ?= latest

.PHONY: adk-build adk-build-cache adk-run adk-teardown adk-auto adk-auto-cache adk-clean maf-build maf-build-cache maf-run maf-teardown maf-auto maf-auto-cache maf-clean clean build build-cache run teardown auto auto-cache

## Google ADK Targets
# Build the Docker image for ADK
adk-build:
	docker buildx build --no-cache -f $(ADK_DOCKERFILE) -t $(ADK_IMAGE_NAME):$(ADK_TAG) --load .

# Build the Docker image for ADK with cache
adk-build-cache:
	docker buildx build -f $(ADK_DOCKERFILE) -t $(ADK_IMAGE_NAME):$(ADK_TAG) --load .

# Run the Docker container using Docker Compose
adk-run:
	docker compose -f $(ADK_COMPOSEFILE) up -d

# Stop the Docker container using Docker Compose
adk-teardown:
	docker compose -f $(ADK_COMPOSEFILE) down

# Auto build and run
adk-auto: adk-build adk-run

# Auto build with cache and run
adk-auto-cache: adk-build-cache adk-run

# Clean up Docker images related to this project
adk-clean:
	docker rmi $(ADK_IMAGE_NAME):$(ADK_TAG) || true

## Microsoft AF Targets
# Build the Docker image for MAF
maf-build:
	docker buildx build --no-cache -f $(MAF_DOCKERFILE) -t $(MAF_IMAGE_NAME):$(MAF_TAG) --load .

# Build the Docker image for MAF with cache
maf-build-cache:
	docker buildx build -f $(MAF_DOCKERFILE) -t $(MAF_IMAGE_NAME):$(MAF_TAG) --load .

# Run the Docker container using Docker Compose
maf-run:
	docker compose -f $(MAF_COMPOSEFILE) up -d

# Stop the Docker container using Docker Compose
maf-teardown:
	docker compose -f $(MAF_COMPOSEFILE) down

# Auto build and run
maf-auto: maf-build maf-run

# Auto build with cache and run
maf-auto-cache: maf-build-cache maf-run

# Clean up Docker images related to this project
maf-clean:
	docker rmi $(MAF_IMAGE_NAME):$(MAF_TAG) || true

## General Targets
# Clean up all Docker images related to this project
clean: adk-clean maf-clean

# Build all Docker images
build: adk-build maf-build

# Build all Docker images with cache
build-cache: adk-build-cache maf-build-cache

# Run all Docker containers
run: adk-run maf-run

# Teardown all Docker containers
teardown: adk-teardown maf-teardown

# Auto build and run all Docker containers
auto: adk-auto maf-auto

# Auto build with cache and run all Docker containers
auto-cache: adk-auto-cache maf-auto-cache
