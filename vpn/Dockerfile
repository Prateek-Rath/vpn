FROM python:3.11-slim

WORKDIR /vpn

COPY *.py ./ 

COPY static ./static

RUN pip install --no-cache-dir fastapi uvicorn httpx PyJWT prometheus_client

EXPOSE 9001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9001"]
