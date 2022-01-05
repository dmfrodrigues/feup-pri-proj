FROM solr:8.10

COPY /data/combined.csv /data/combined.csv

COPY /schema/schema.json /data/schema.json

COPY /config/startup.sh /scripts/startup.sh

COPY /config/web.xml /opt/solr-8.10.1/server/solr-webapp/webapp/WEB-INF/

COPY /config/jetty-servlet-9.4.44.v20210927.jar /opt/solr-8.10.1/server/solr-webapp/webapp/WEB-INF/lib/

ENTRYPOINT ["/scripts/startup.sh"]
