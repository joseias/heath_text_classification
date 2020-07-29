import re
import json
import os

import pandas as pd
from tqdm import tqdm

def load_text(path):
    docs = []

    # _=root, _=directories, f = files
    for _, _, f in os.walk(path):
        for file in tqdm(f):
            fpath = os.path.join(path, file)
            with open(fpath) as fs:
                doc = json.load(fs)
                id = doc["paper_id"]
                text = [textpart["text"] for textpart in doc["body_text"]]
                if len(text) > 0:
                    text = " ".join(text) 
                    
                    # remove some extra "\n" in some documents
                    text = re.sub(r"[\n]{1,}", " ", text).strip()
                    docs.append((id, text))
                else:
                    print("Missing text -> ",fpath)
                    
    df = pd.DataFrame(docs, columns=["id", "text"])
    return df



path = "./pmc_json"
outpath = "cord19_20200728.csv"
df = load_text(path)
df.to_csv(outpath, index=False)
print("Done...")