FROM python:3.13.0
WORKDIR /backend
ADD . .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg lsb-release && \
    # Docker 공식 GPG 키 & 레포 등록
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
        gpg --dearmor -o /usr/share/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) \
        signed-by=/usr/share/keyrings/docker.gpg] \
        https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" \
        > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    # docker-ce-cli 만 설치 (엔진 X)
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8011
CMD ["python", "main.py"]