#!/bin/bash

# Change directory to script directory
# This uses readlink so symlinks dont break it
cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

# Run a local webserver on port 8000
python -m http.server 8000