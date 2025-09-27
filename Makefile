# Variables
DOCKERFILE ?= Dockerfile
IMAGE_NAME ?= chatbot-template
TAG ?= latest

# Default target
.PHONY: build clean run

build:
	docker buildx build --no-cache -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) --load .

build-cache:
	docker buildx build -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) --load .

# Run the Docker container using Docker Compose
run:
	docker compose up -d

# Stop the Docker container using Docker Compose
teardown:
	docker compose down

# Auto build and run
auto: build run

# Auto build with cache and run
auto-cache: build-cache run

# Clean up Docker images related to this project
clean:
	docker rmi $(IMAGE_NAME):$(TAG) || true
