FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap socat tcpdump iputils-ping iproute2 curl && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pymodbus==3.6.9
CMD ["socat", "TCP-LISTEN:8080,fork,reuseaddr", "TCP:10.250.10.11:8080"]
