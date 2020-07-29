import re
import pandas as pd

def load_text(path):
    MIN_TEXT_LENGTH = 200

    # read the data
    with open(path) as fs:
        # read all the content, this is very inefficient
        content = fs.read() 
        # workaround for some documents using four \n as separator instead of 3
        docs = []
        # split documents [\n]{4,} can be used as separator
        for rawdoc in re.split(r"[\n]{4,}", content):
            # split by "\n\n", field separator
            doc = re.split(r"[\n]{2,}", rawdoc)
            # get PMID (must be the last one)
            id = doc[len(doc)-1]
            assert id.startswith("PMID:"), str(id)
            id = id.split(" ")
            id = id[0]+id[1]

            # sort by lenght, text must be the longest
            doc = sorted(doc, key=len, reverse=True)

            # remove some extra "\n" in some documents
            text = re.sub(r"[\n]{1,}", " ", doc[0]).strip()

            # text is missin in some documents...
            if len(text) > MIN_TEXT_LENGTH:
                docs.append((id,text))

    df = pd.DataFrame(docs, columns=["id", "text"])
    return df



inpath = "yeast_abbrev_unlabeled.txt"
outpath = "yeast_abbrev_unlabeled.csv"
df = load_text(inpath)
df.to_csv(outpath, index=False)

