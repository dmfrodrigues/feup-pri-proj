FROM solr:8.10

COPY /data/combined.csv /data/combined.csv

COPY /schema/schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]
