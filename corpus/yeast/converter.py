import re
import pandas as pd

def load_yeast_abb(path):
    MIN_TEXT_LENGTH = 200

    # read the data
    with open(path) as f:
        # read all the content, this is very inefficient
        content = f.read() 
        # workaround for some documents using four \n as separator instead of 3
        docs = []
        # split by "PMID:", as document separator
        for rawdoc in re.split(r"[\n]{3,}", content):
            # split by "\n\n", field separator
            doc = re.split(r"[\n]{2,}", rawdoc)
            
            # sort by lenght, text must be the longest
            doc = sorted(doc, key=len, reverse=True)

            # remove some extra "\n" in some documents, for example titles spawning more than one row
            text = re.sub(r"[\n]{1,}", " ", doc[0]).strip()

            # text is missin in some documents...
            if len(text) > MIN_TEXT_LENGTH:
                docs.append(text)

    df = pd.DataFrame(docs, columns=["text"])
    return df

def load_pudmed():
    return None

inpath = "yeast_abbrev_unlabeled.txt"
outpath = "yeast_abbrev_unlabeled.csv"

df = load_yeast_abb(inpath)
df.to_csv(outpath, index=False)