# if you dont have kind cluster installed, run:
kind create cluster  --config kind-config.yaml

kubectl apply -f k8s/
kubectl port-forward service/frontend 8501:8501