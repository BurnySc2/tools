set -a

source .env

nimble c -r -d:ssl -o:main src/main.nim
# nim r -d:ssl src/main.nim
# nim c -r -d:ssl -d:release main.nim
# nim c -r -d:ssl -d:danger main.nim
