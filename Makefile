VERSION ?= latest
REGISTRY ?= registry.rickokkersen.nl/underlyingglitch

dep: docker deploy

deploy: 
	kubectl rollout restart deployment deployment-agent --namespace=laravel-applications

docker: docker-build docker-push

docker-build:
	docker build . -t ${REGISTRY}/k8s-github-agent:${VERSION}
	
docker-push:
	docker push ${REGISTRY}/k8s-github-agent:${VERSION}