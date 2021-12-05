import re
import sys, json, csv

CELEX_REGEX = re.compile(r"http:\/\/eur-lex\.europa\.eu\/LexUriServ\/LexUriServ\.do\?uri=CELEX:([a-zA-Z0-9\(\)\-]+):EN:NOT")
def get_celex_from_url(url):
    m = CELEX_REGEX.match(url)
    try:
        ret = m.group(1)
        return ret
    except:
        return None

CELEX_REL_REGEX = re.compile(r"http:\/\/eur-lex\.europa\.eu\/Result\.do\?RechType=RECH_celex&amp;lang=en&amp;code=([a-zA-Z0-9\(\)\-]*)")
def get_celex_from_url_rel(url):
    m = CELEX_REL_REGEX.match(url)
    try:
        ret = m.group(1)
        return ret
    except:
        return None

def process_date(date: str) -> str:
    if date == "": return ""
    if date.endswith("00"): return ""
    return date

def process_ofeffect_date(date: str) -> str:
    date = process_date(date)
    if date == "": return ""
    if date > "3000-00-00": return ""
    return date

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

    rels = []
    for rel in entry["relationships"]:
        rel_link = rel["link"]
        if rel_link == '': continue

        if rel_link.startswith("http://eur-lex.europa.eu/http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CONSLEG"): continue
        if rel_link == "http://eur-lex.europa.eu/Result.do?RechType=RECH_celex&amp;lang=en&amp;code=[2~192E066": continue

        rel_celex = get_celex_from_url_rel(rel_link)
        if rel_celex == '': continue
        if rel_celex == None:
            print(f"CELEX {celex}, FAILED TO MATCH REL {rel_link}", file=sys.stderr)
        else:
            rels.append(rel_celex)

    newEntry = {
        "celex": celex,
        
        "form": entry["form"],
        "date": entry["date_document"],
        
        "title": (entry["title"] if entry["title"] != "\u00a0" else ""),
        
        "oj_date": process_date(entry["oj_date"]),
        "of_effect": process_ofeffect_date(entry["of_effect"]),
        "end_validity": process_date(entry["end_validity"]),
        
        "addressee": entry["addressee"],

        "subject_matter": [v["subject_matter"] for v in entry["subject_matter"]],
        "directory_codes": [v["directory_code"] for v in entry["directory_codes"]],
        "eurovoc_descriptors": [v["eurovoc_descriptor"] for v in entry["eurovoc_descriptors"]],
        "legal_basis": [v["legal_basis"] for v in entry["legal_basis"]],
        "relationships": rels
    }

    if celex in data:
        print(f"WARNING: Document with CELEX {celex} was already in data; overwritting", file=sys.stderr)

    data[celex] = newEntry

# Fix individual items
if data["22005A0312(01)"]["of_effect"] == "2005-00-20": data["22005A0312(01)"]["of_effect"] = "2005-02-01"

LEGAL_BASIS_REPLACEMENTS = {
}

for celex in data:
    # LEGAL_BASIS
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
            # print("{}: legal basis {} not available".format(celex, basis), file=sys.stderr)
            # if re.match(r'([a-zA-Z0-9\(\)\-\/]+)', basis) == None:
            #     print("{}: legal basis {} not available and is strange".format(celex, basis), file=sys.stderr)
            pass
    
    data[celex]["legal_basis"] = legal_basis

    # RELATIONSHIPS
    relationships_old = data[celex]["relationships"]
    relationships = []

    for s in relationships_old:
        if s == "" or s == "-" or s == "[2~192E066": continue

        m = re.match(r'([a-zA-Z0-9\(\)\-\/]+)( )*[\-]+.*', s)
        if m != None: relationships.append(m.group(1)); continue
        
        if s in LEGAL_BASIS_REPLACEMENTS: relationships.append(LEGAL_BASIS_REPLACEMENTS[s]); continue

        relationships.append(s)
    
    for rel in relationships:
        if rel not in data:
            # print("{}: relationship {} not available".format(celex, rel), file=sys.stderr)
            # if re.match(r'([a-zA-Z0-9\(\)\-\/]+)', rel) == None:
            #     print("{}: relationship {} not available and is strange".format(celex, rel), file=sys.stderr)
            pass
    
    data[celex]["relationships"] = relationships

    # OTHERS
    assert "".join(data[celex]["subject_matter"     ]).find(";") == -1
    assert "".join(data[celex]["directory_codes"    ]).find(";") == -1
    assert "".join(data[celex]["eurovoc_descriptors"]).find(";") == -1
    assert "".join(data[celex]["legal_basis"        ]).find(";") == -1
    assert "".join(data[celex]["relationships"      ]).find(";") == -1

    data[celex]["subject_matter"     ] = ";".join(data[celex]["subject_matter"     ])
    data[celex]["directory_codes"    ] = ";".join(data[celex]["directory_codes"    ])
    data[celex]["eurovoc_descriptors"] = ";".join(data[celex]["eurovoc_descriptors"])
    data[celex]["legal_basis"        ] = ";".join(data[celex]["legal_basis"        ])
    data[celex]["relationships"      ] = ";".join(data[celex]["relationships"      ])

    w.writerow([data[celex][col] for col in columns])
