FROM python:3.13.0
WORKDIR /backend
ADD . .
ARG MCP_VERSION=v0.4
RUN curl -L -o /usr/local/bin/github-mcp-server \
    https://github.com/github/github-mcp-server/releases/download/${MCP_VERSION}/github-mcp-server_linux_amd64 && \
    chmod +x /usr/local/bin/github-mcp-server
RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8011
CMD ["python", "main.py"]