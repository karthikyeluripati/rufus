# Rufus Deployment Guide

## Local Deployment

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Set environment variables:
```bash
export RUFUS_API_KEY=your_api_key
export RUFUS_MAX_DEPTH=3
```

3. Run the application:
```bash
streamlit run src/frontend/app.py
```

## Streamlit Cloud Deployment

1. Push code to GitHub repository

2. Connect to Streamlit Cloud:
   - Visit https://share.streamlit.io/
   - Connect your GitHub account
   - Select your repository

3. Configure secrets in Streamlit Cloud:
   - Go to App Settings > Secrets
   - Add your environment variables:
     ```
     RUFUS_API_KEY=your_api_key
     ```

4. Add `packages.txt` for system dependencies:
```
# packages.txt
chromium
```

5. Update `requirements.txt` to use compatible versions:
```
aiohttp>=3.9.1
beautifulsoup4>=4.12.2
fastapi>=0.109.1
langchain>=0.1.0
loguru>=0.7.2
openai>=1.3.7
playwright>=1.41.1
pydantic>=2.5.2
python-dotenv>=1.0.0
streamlit>=1.29.0
```

## Docker Deployment

1. Create Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium

COPY src/ src/

EXPOSE 8501

CMD ["streamlit", "run", "src/frontend/app.py"]
```

2. Build and run:
```bash
docker build -t rufus .
docker run -p 8501:8501 rufus
```

## Kubernetes Deployment

1. Create deployment.yaml:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rufus
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rufus
  template:
    metadata:
      labels:
        app: rufus
    spec:
      containers:
      - name: rufus
        image: rufus:latest
        ports:
        - containerPort: 8501
        env:
        - name: RUFUS_API_KEY
          valueFrom:
            secretKeyRef:
              name: rufus-secrets
              key: api-key
```

2. Apply configuration:
```bash
kubectl apply -f deployment.yaml
```

## Monitoring

1. Set up logging:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

2. Configure metrics:
```python
from prometheus_client import Counter, Histogram
requests_total = Counter('requests_total', 'Total requests')
```

## Scaling

1. Configure Redis for caching:
```python
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
```

2. Set up load balancer:
```nginx
upstream rufus {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
}
```

## Backup and Recovery

1. Database backups:
```bash
redis-cli save
```

2. Configuration backups:
```bash
kubectl get configmap -o yaml > config-backup.yaml
```

## Security

1. Enable HTTPS:
```python
ssl_cert = "/path/to/cert.pem"
ssl_key = "/path/to/key.pem"
```

2. Set up authentication:
```python
streamlit_auth = {
    'credentials': {
        'usernames': {
            'admin': 'password'
        }
    }
}
```

## Performance Optimization

1. Enable caching:
```python
@st.cache_data
def fetch_data():
    pass
```

2. Configure thread pool:
```python
import concurrent.futures
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
```