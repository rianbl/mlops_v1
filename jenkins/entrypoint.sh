#!/bin/bash
set -e

DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)

# Cria grupo docker se não existir
if ! getent group docker >/dev/null; then
    groupadd -g "$DOCKER_GID" docker
fi

# Adiciona jenkins ao grupo docker
usermod -aG docker jenkins

# Executa o Jenkins como usuário jenkins
exec gosu jenkins /usr/bin/tini -- /usr/local/bin/jenkins.sh
