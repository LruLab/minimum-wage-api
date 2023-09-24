#!/bin/bash -e

poetry export --without-hashes -o requirements.txt

vercel .