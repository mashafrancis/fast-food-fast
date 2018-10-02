TAG = $(shell git rev-parse --short HEAD)
PROJECT = sandbox-kube
IMAGE = us.gcr.io/$(PROJECT)/swagger
pwd = $(shell pwd)
export HOST_IP=$(shell ipconfig getifaddr en0 || ipconfig getifaddr en1)
export TAG=$(shell git rev-parse --short HEAD)


image:
	docker build -t $(IMAGE):$(TAG) -t $(IMAGE):latest .

push: image
	gcloud docker -- push $(IMAGE):$(TAG) && gcloud docker -- push $(IMAGE):latest

deploy: push
	kubectl set image deployment/api-docs api-docs=$(IMAGE):$(TAG)

deploy_stage:
	make deploy PROJECT=microservices-kube

deploy_prod:
	make deploy PROJECT=andela-kube