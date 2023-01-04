source config.sh
docker run -d --rm --name "$REDIS_CONTAINER_NAME" -p "$REDIS_CONTAINER_HOST":"$REDIS_CONTAINER_PORT":"$REDIS_CONTAINER_PORT" redis:latest

