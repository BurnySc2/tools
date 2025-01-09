FROM nimlang/nim:2.2.0-alpine as base

# Install dependencies
COPY twitch_stream_announcer.nimble /root/tsa/
WORKDIR /root/tsa
RUN nimble install --depsOnly

# Build binary
COPY src /root/tsa/src
# RUN nimble c -d:ssl -d:release --passL:"-static -no-pie" -o:main src/main.nim 
RUN nimble c -d:ssl -o:main src/main.nim 
# RUN nimble c -d:ssl -d:danger-o:main src/main.nim 

# # Squash image with trick https://stackoverflow.com/a/56118557/10882657
# FROM alpine:3
# RUN mkdir -p /root/tsa
# COPY --from=base /root/tsa/main /root/tsa/main

# How to get the .so without installing the whole lib?
# https://pkgs.alpinelinux.org/package/edge/main/x86/libpq
RUN apk add libpq
# RUN apk add openssl
# RUN apk add libssl3

WORKDIR /root/tsa
CMD ["./main"]
