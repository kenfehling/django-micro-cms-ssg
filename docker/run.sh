HOST_APPDIR="$(pwd)"/..
GUEST_APPDIR=/app

docker build -t dmcs:latest .

docker run -i -t \
    --mount type=bind,source=$HOST_APPDIR,target=$GUEST_APPDIR \
    -v $(readlink -f $SSH_AUTH_SOCK):/ssh-agent \
    -e SSH_AUTH_SOCK=/ssh-agent \
    -p 8000:8000 \
    dmcs:latest
