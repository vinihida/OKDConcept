# FastAPI OKD POC (KISS)

Prova de conceito simples para demonstrar:

- containerizacao
- deploy em Kubernetes/OKD
- escalabilidade (replicas)
- variaveis de ambiente
- healthcheck
- logs basicos

## Endpoints

- `GET /` -> mensagem e hostname do pod
- `GET /health` -> status OK
- `GET /env` -> variaveis de ambiente relevantes
- `GET /counter` -> contador em memoria (incrementa por pod)

## Rodar local

```bash
pip install -r requirements.txt
set PORT=8000
uvicorn main:app --host 0.0.0.0 --port %PORT%
```

## Build da imagem

```bash
docker build -t okd-poc:latest .
```

## Deploy no cluster

Atualize a imagem em `k8s/deployment.yaml`:

`your-registry/okd-poc:latest`

Depois aplique:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/route.yaml
```

## Escalar

```bash
kubectl scale deployment okd-poc --replicas=4
```

## Observabilidade basica

```bash
kubectl logs -l app=okd-poc -f
kubectl get pods -l app=okd-poc -o wide
```
