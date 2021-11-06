import re
import sys, json, csv

CELEX_REGEX = re.compile("http:\/\/eur-lex\.europa\.eu\/LexUriServ\/LexUriServ\.do\?uri=CELEX:([a-zA-Z0-9\(\)\-]+):EN:NOT")
def get_celex_from_url(url):
    m = CELEX_REGEX.match(url)
    ret = m.group(1)
    return ret

input_data = json.load(sys.stdin)

columns = [
    "celex",
    "form",
    "date",
    "title",
    "oj_date",
    "of_effect",
    "end_validity",
    "addressee",
    "subject_matter",
    "directory_codes",
    "eurovoc_descriptors",
    "legal_basis",
    "relationships"
]

w = csv.writer(sys.stdout)
w.writerow(columns)

data = dict()

for key in input_data:
    entry = input_data[key]

    url = entry["eurlex_perma_url"]
    celex = get_celex_from_url(url)

    newEntry = {
        "celex": celex,
        
        "form": "Agreement",
        "date": entry["date_document"],
        
        "title": entry["title"],
        
        "oj_date": entry["oj_date"],
        "of_effect": entry["of_effect"],
        "end_validity": entry["end_validity"],
        
        "addressee": entry["addressee"],
        "subject_matter": [v["subject_matter"] for v in entry["subject_matter"]],
    
        "directory_codes": [v["directory_code"] for v in entry["directory_codes"]],
        "eurovoc_descriptors": [v["eurovoc_descriptor"] for v in entry["eurovoc_descriptors"]],
        "legal_basis": [v["legal_basis"] for v in entry["legal_basis"]],
        "relationships": entry["relationships"],
    }

    data[celex] = newEntry

LEGAL_BASIS_REPLACEMENTS = {
}

for celex in data:
    legal_basis_old = data[celex]["legal_basis"]
    legal_basis = []

    for s in legal_basis_old:
        if s == "" or s == "-" or s == "[2~192E066": continue

        m = re.match(r'([a-zA-Z0-9\(\)\-\/]+)( )*[\-]+.*', s)
        if m != None: legal_basis.append(m.group(1)); continue
        
        if s in LEGAL_BASIS_REPLACEMENTS: legal_basis.append(LEGAL_BASIS_REPLACEMENTS[s]); continue

        legal_basis.append(s)
    
    for basis in legal_basis:
        if basis not in data:
            print("{}: legal basis {} not available".format(celex, basis), file=sys.stderr)
            # if re.match(r'([a-zA-Z0-9\(\)\-\/]+)', basis) == None:
            #     print("{}: legal basis {} not available and is strange".format(celex, basis), file=sys.stderr)
            pass
    
    data[celex]["legal_basis"] = legal_basis

    assert "".join(data[celex]["directory_codes"    ]).find(";") == -1
    assert "".join(data[celex]["eurovoc_descriptors"]).find(";") == -1
    assert "".join(data[celex]["legal_basis"        ]).find(";") == -1

    data[celex]["directory_codes"    ] = ";".join(data[celex]["directory_codes"    ])
    data[celex]["eurovoc_descriptors"] = ";".join(data[celex]["eurovoc_descriptors"])
    data[celex]["legal_basis"        ] = ";".join(data[celex]["legal_basis"        ])

    w.writerow([data[celex][col] for col in columns])
