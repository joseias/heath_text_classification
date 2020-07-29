import pandas as pd

def load_yeast_abb(path):
    # read the data
    sep = "\n"

    SOURCE = "source"
    TITLE = "title"
    AUTHORS = "authors"
    INST = "institution"
    TEXT = "text"
    REF = "ref"
    NEWDOC1 = "newdoc1"
    NEWDOC2 = "newdoc2"

    trans = {SOURCE:TITLE, 
            TITLE:AUTHORS, 
            AUTHORS:INST, 
            INST:TEXT,
            TEXT:REF,
            REF:NEWDOC1,
            NEWDOC1:NEWDOC2,
            NEWDOC2:SOURCE}
            
    exs = set([NEWDOC1, NEWDOC2])

    docs = []
    with open(path) as f:
        doc = {SOURCE:[], TITLE:[], AUTHORS:[], INST:[], TEXT:[], REF:[]}
        state = SOURCE
        for line in f:
            if line != sep:
                if state not in exs:
                    doc[state].append(line.replace("\n",""))
            else:
                if state == REF:
                    for key in doc.keys():
                        doc[key] = " ".join(doc[key])
                    docs.append(doc)
                    doc = {SOURCE:[], TITLE:[], AUTHORS:[], INST:[], TEXT:[], REF:[]}        
                state = trans[state]
        # add the last doc since there is no blank line at the EOF
        docs.append(doc)

    df = pd.DataFrame(docs, columns=[SOURCE, TITLE, AUTHORS, INST, TEXT, REF])
    return df

def load_pudmed():
    return None

path = "E:\\Work\\01_DL\\05_UA\\TextClassification\\Corpus\\yeast_abbrev_unlabeled.txt"
df = load_yeast_abb(path)
print(df.shape)
df.to_csv("E:\\Work\\01_DL\\05_UA\\TextClassification\\Corpus\\yeast_abbrev_unlabeled.csv", index=False)