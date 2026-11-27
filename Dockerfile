FROM debian:trixie

COPY raspberrypi-archive-keyring.pgp /usr/share/keyrings/
COPY raspi.sources /etc/apt/sources.list.d/

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-picamera2 python3-opencv python3-numpy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python3", "capture.py"]
