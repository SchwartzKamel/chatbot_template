# Variables
DOCKERFILE ?= Dockerfile
IMAGE_NAME ?= chatbot-template
TAG ?= latest

# Default target
.PHONY: build clean run

build:
	docker buildx build -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) --load .

# Run the Docker container
run:
	docker run -it --rm -p 8000:8000 --env-file .env $(IMAGE_NAME):$(TAG)

# Clean up Docker images related to this project
clean:
	docker rmi $(IMAGE_NAME):$(TAG) || true
