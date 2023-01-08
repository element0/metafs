source config-redis.sh
docker network create "$REDIS_CONTAINER_NET"
docker run -d --rm --name "$REDIS_CONTAINER_NAME" --network "$REDIS_CONTAINER_NET" -p "$REDIS_CONTAINER_HOST":"$REDIS_CONTAINER_PORT":"$REDIS_CONTAINER_PORT" redis:latest

