# Miscelaneous functions

import time, requests, glob, os
import pandas as pd


def connect(url, time_limit = 15):
    success = False
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    timeout = time.time() + time_limit
    while success==False:
        if time.time() > timeout:
            raise ConnectionError
        try:
            content = requests.get(url, headers=headers, timeout=5)
            success=True
        except:
            pass
    return(content) 

def dir_to_dataframe(path):
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    return(df)

def is_raw_pdf(url, link):
    if url is None or link is None:
        return False
    return(url[3:13].isnumeric() or link.endswith(".pdf"))
