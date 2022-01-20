# Information Retrieval System for European Union Legislation

## How to get data

The data file containing the dataset has 3.44GB not compressed, and even when compressed it has ~400MB, which does not fit in moodle file size restrictions. The `combined.csv` data file is available at https://drive.google.com/drive/folders/1aXdNni0DtbRXS6HDofQAXyDOJcAiB4Ld. You have to download `combined.zip`, unzip it and move file `combined.csv` to path `solr/data`, so that the new file path is `solr/data/combined.csv`.

## Get synonyms

To get synonyms, go to folder `solr/synonyms`, and run `make`. This command works under Ubuntu 20.04.

## How to run

Change current directory to `solr`, and run
```sh
docker-compose up --build
```

To kill the container, use
```sh
docker-compose down
```

Solr is available at port 8984 (<localhost:8984>), the frontend is available at port 8000 (<localhost:8000>).
