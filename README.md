# Information Retrieval System for European Union Legislation

## How to get data

The data file containing the dataset has 1.31GB not compressed, and even when compressed it has ~400MB, which does not fit in moodle file size restrictions. The `combined.csv` data file is available at https://drive.google.com/drive/folders/1aXdNni0DtbRXS6HDofQAXyDOJcAiB4Ld. You have to download `combined.zip`, unzip it and move file `combined.csv` to path `solr/data`, so that the new file path is `solr/data/combined.csv`.

## How to run

Change current directory to `solr`, and run
```sh
docker-compose up --build
```

To kill the container, use
```sh
docker-compose down
```
