#!/bin/bash

export FLASK_ENV=development
export OAUTHLIB_INSECURE_TRANSPORT=1

docker run -d -p 3005:3000 --name metabase metabase/metabase

# default behavior of DATASTORE_EMULATOR_HOST being set to values like `::1:8971` doesn't seem to work, so rewrite it.
$(gcloud beta emulators datastore env-init)
port=${DATASTORE_EMULATOR_HOST##*:}
export DATASTORE_EMULATOR_HOST="localhost:${port}"

python src/main.py
