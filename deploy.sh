#!/bin/bash -e

# build docs
npx @redocly/cli build-docs -o doc/index.html

# export requirements.txt
poetry export --without-hashes -o requirements.txt

vercel .