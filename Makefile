# Variables
DOCKERFILE ?= Dockerfile
IMAGE_NAME ?= chatbot-template
TAG ?= latest

# Default target
.PHONY: build
build:
	docker buildx build -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) --load .

# Clean up dangling images
.PHONY: clean
clean:
	docker image prune -f