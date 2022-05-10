# Information Retrieval System for European Union Legislation

- **Project name:** Information Retrieval System for European Union Legislation
- **Short description:** Built on Solr, with a custom frontend, system used to retrieve information from the European Union Legislation, provided by [EUR-Lex](https://eur-lex.europa.eu/homepage.html)
- **Environment:** Browser
- **Tools:** Python, Solr, HTML/JS/CSS
- **Institution:** [FEUP](https://sigarra.up.pt/feup/en/web_page.Inicial)
- **Course:** [PRI](https://sigarra.up.pt/feup/en/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=486244) (Information Processing and Retrieval)
- **Project grade:** 19.2/20.0
- **Group members:**
    - [Diogo Miguel Ferreira Rodrigues](https://github.com/dmfrodrigues) (<dmfrodrigues2000@gmail.com> / <diogo.rodrigues@fe.up.pt>)
    - [João Sousa](https://github.com/JoaoASousa) ([up201806613@fe.up.pt](mailto:up201806613@fe.up.pt))
    - [Rafael Soares Ribeiro](https://github.com/up201806330) (<up201806330@fe.up.pt>)

## How to get data

The data file containing the dataset is 3.44GB uncompressed, and even when compressed is ~400MB, which does not fit in moodle file size restrictions. The `combined.csv` data file is available at https://drive.google.com/drive/folders/1aXdNni0DtbRXS6HDofQAXyDOJcAiB4Ld. You have to download `combined.zip`, unzip it and move file `combined.csv` to path `solr/data`, so that the new file path is `solr/data/combined.csv`.

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

Solr is available at port 8983 (<localhost:8983>), the frontend is available at port 8000 (<localhost:8000>).
