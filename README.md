# Proost

For now the main repo for Proost. Functionality should be split up in separate components. This
repo will start with pumping data from Google Calendar to a database.

## Bring up local

Get `google_client_secret.json` and put it in `/server/src`.

Run:

```
cd server
virtualenv -p python3 .virtualenv
source .virtualenv/bin/activate
./install_deps.sh
./run_datastore.sh
```

In a separate shell:

```
./run_local.sh
```

TODO: Run everything with a single command in a single shell.
