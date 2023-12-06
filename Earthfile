VERSION 0.6
ARG PYTHONVERSION=3.11 # 3.10 to 3.11
ARG NIMVERSION=2.0.0
FROM alpine:3.15 # Is only used for formatting, so image can be as small as possible

# Run autoformatter on all projects
format:
    BUILD ./burny_common+format
    BUILD ./discord_bot+format
    BUILD ./fastapi_server+format
    BUILD ./python_examples+format
    BUILD ./transcribe_website/transcriber_backend+format

install-all:
    BUILD ./burny_common+install-dev --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./discord_bot+install-dev --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./fastapi_server+install-dev --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./python_examples+install-dev --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./transcribe_website/transcriber_backend+install-dev --PYTHONVERSION=3.10

pre-commit:
    BUILD ./burny_common+pre-commit --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./discord_bot+pre-commit --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./fastapi_server+pre-commit --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./python_examples+pre-commit --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./transcribe_website/transcriber_backend+pre-commit --PYTHONVERSION=3.10

check-all:
    BUILD ./burny_common+all --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./discord_bot+all --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./fastapi_server+all --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./python_examples+all --PYTHONVERSION=${PYTHONVERSION}
    BUILD ./transcribe_website/transcriber_backend+all --PYTHONVERSION=3.10
    BUILD ./nim_examples+all --NIMVERSION=${NIMVERSION}

# Run format-checks, linter and tests
all:
    BUILD +check-all
