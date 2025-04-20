# TECH CHALLENGE 5

## Microsserviços no EKS

| Serviço              | Função                                                                  |
|----------------------|-------------------------------------------------------------------------|
| video-uploader       | Recebe vídeos do frontend e envia metadados para a fila SQS              |
| video-processor      | Escuta SQS, processa vídeos do S3, atualiza status e envia notificação   |
| status-service       | Consulta e atualiza status dos vídeos no DynamoDB                       |
| notification-service  | Publica mensagens no SNS para notificar o usuário                        |
| auth-service         | Autentica usuários com AWS Cognito e retorna JWT                        |

Esses serviços rodam em containers no **EKS** e se comunicam por **HTTP interno** ou por eventos via **SQS/SNS**.

---

## Fluxo de Autenticação

- Usuário se autentica via **Amazon Cognito**
- Recebe um **JWT**
- JWT é incluído nas requisições como `Authorization: Bearer <token>`

---

## Upload do Vídeo

1. Frontend faz `PUT` via **presigned URL gerado pelo backend**
2. Vídeo é salvo no **S3**
3. Frontend notifica o backend, que envia metadados para o **SQS**

---

## Processamento do Vídeo

1. `video-processor` consome do SQS
2. Baixa o vídeo do S3
3. Extrai imagens / gera `.zip`
4. Atualiza status no **DynamoDB**
5. Publica evento no **SNS**

---

## Notificação

- `notification-service` consome SNS e envia e-mail para o usuário com o status final

---

## Serviços AWS Utilizados

### Cognito

- User Pool + App Client
- Habilitar `ALLOW_USER_PASSWORD_AUTH` e `ALLOW_REFRESH_TOKEN_AUTH`

### S3

- Bucket: `tech5-dev-videos`
- Armazena os vídeos enviados

### SQS

- Fila: `tech5-dev-video-queue`
- Enfileira requisições para o `video-processor`

### DynamoDB

- Tabela: `tech5-dev-video-status`
- Chave primária: `video_id`
- GSI: `user_id-index`

### SNS

- Tópico: `tech5-dev-video-topic`
- Assinantes: e-mail (usuário)

---

## Deploy no EKS

### 1. Subir imagens para o ECR

```bash
docker build -t <serviço> .
docker tag <serviço>:latest 973181171011.dkr.ecr.us-east-1.amazonaws.com/<serviço>:latest
docker push 973181171011.dkr.ecr.us-east-1.amazonaws.com/<serviço>:latest
```

### 2. Criar o cluster EKS (via Terraform ou Console)

### 3. Criar roles com trust policy OIDC (IRSA)

- Exemplo de trust:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<account_id>:oidc-provider/<eks_oidc_provider>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<eks_oidc_provider>:sub": "system:serviceaccount:default:<serviceaccount>"
        }
      }
    }
  ]
}
```

- Atribuir permissões adequadas por serviço (S3, SQS, DynamoDB, SNS)

### 4. Criar service accounts e anotar

```bash
kubectl create sa <serviceaccount>
kubectl annotate sa <serviceaccount> \
  eks.amazonaws.com/role-arn=arn:aws:iam::<account_id>:role/<role-name>
```

### 5. Aplicar arquivos de deployment YAML

```bash
kubectl apply -f <serviço>-deployment.yaml
```

### 6. Verificar services e LoadBalancers

```bash
kubectl get svc
```

---

## Testes via cURL

### Login via Cognito

```bash
curl -X POST http://<auth-service-lb>:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"paulo", "password":"Senha123@"}'
```

### Upload de vídeo

```bash
curl -F "file=@/caminho/do/video.mp4" http://<video-uploader-lb>:8002/upload/
```

### Consulta status

```bash
curl http://<status-service-lb>:8003/videos/<user_id>
```

### Envio manual de notificação

```bash
curl -X POST http://<notification-service-lb>:8004/notify \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@teste.com",
    "status": "done",
    "video_id": "xyz123"
}'
```

---

## Comandos Frequentes

### Dependências Python

```bash
pip install -r requirements.txt
```

### Docker Compose (para dev local)

```bash
docker compose down -v
docker compose up --build -d
```

### Makefile (opcional)

```bash
make up                # Sobe tudo
make logs              # Logs de todos os serviços
make terraform-apply   # Aplica a infra
make test-status       # Testa status-service
```

---

## Organização do Projeto

```sh
.
├── docker-compose.yml
├── video-uploader/
├── video-processor/
├── status-service/
├── notification-service/
├── auth-service/
└── infra/            # Terraform para AWS
```
