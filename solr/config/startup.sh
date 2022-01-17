#!/bin/bash

precreate-core docs

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 2

# Add synonyms
mkdir -p /var/solr/data/docs/res/
cp /data/synonyms.txt /var/solr/data/docs/res/synonyms.txt
echo "Added synonyms"

# Schema definition via API
STARTTIME=$(date +%s)
curl -s -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/docs/schema
ENDTIME=$(date +%s)
echo "Defined schema: $(($ENDTIME - $STARTTIME)) seconds"

# Populate collection

STARTTIME=$(date +%s)
curl -s -X POST 'http://localhost:8983/solr/docs/update/csv?commit=true&encapsulator="' \
    -T /data/combined.csv \
    -H 'Content-type:application/csv'
ENDTIME=$(date +%s)
echo "Uploaded csv: $(($ENDTIME - $STARTTIME)) seconds"

sleep 2

# Restart in foreground mode so we can access the interface
solr restart -f
