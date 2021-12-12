#!/bin/bash

precreate-core docs

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 2

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/docs/schema

# Populate collection

STARTTIME=$(date +%s)

curl -X POST 'http://localhost:8983/solr/docs/update/csv?commit=true&encapsulator="' \
    -T /data/combined.csv \
    -H 'Content-type:application/csv'

ENDTIME=$(date +%s)
echo "Upload csv: $(($ENDTIME - $STARTTIME)) seconds"


sleep 2

# Restart in foreground mode so we can access the interface
solr restart -f
