#!/bin/bash

precreate-core docs

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 2

# Schema definition via API
# curl -X POST -H 'Content-type:application/json' \
#     --data-binary @/data/schema.json \
#     http://localhost:8983/solr/courses/schema

# Populate collection
curl 'http://localhost:8983/solr/docs/update/csv?commit=true&encapsulator="' \
    --data-binary @/data/combined.csv \
    -H 'Content-type:application/csv'

sleep 2

# Restart in foreground mode so we can access the interface
solr restart -f
