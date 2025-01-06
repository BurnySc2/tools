set -a

source .env

nim c -r -d:ssl main.nim
# nim c -r -d:ssl -d:release main.nim
# nim c -r -d:ssl -d:danger main.nim
