# Builds OpenPLC v3 from source (needs internet at BUILD time only).
# If the build fails, check the project's own Dockerfile/install.sh options.
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    git sudo ca-certificates iproute2 && rm -rf /var/lib/apt/lists/*
WORKDIR /workdir
RUN git clone --depth 1 --recursive https://github.com/thiagoralves/OpenPLC_v3.git
WORKDIR /workdir/OpenPLC_v3
RUN ./install.sh docker
EXPOSE 8080 502
CMD ["bash", "./start_openplc.sh"]
