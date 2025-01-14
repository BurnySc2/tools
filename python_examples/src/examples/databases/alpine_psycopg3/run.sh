docker build -t temp .

# Compress image with slim
slim build --target temp --tag temp_slim --http-probe=false --env-file "../../../../.env" --exec "python /root/main.py"
# Ideally the following but it doesnt work, missing imports
# slim build --target temp --tag temp_slim --http-probe=false --env STAGE=BUILD --exec "python /root/main.py"

docker run --rm -it --env-file "../../../../.env" temp_slim
