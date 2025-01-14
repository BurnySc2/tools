docker build -t temp .
docker run --rm -it --env-file "../../../../.env" temp
