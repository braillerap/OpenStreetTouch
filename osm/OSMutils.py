import iso639

def omsutils_get_iso639_code ():
    isolist = [lg.pt1 for lg in iso639.iter_langs() if lg.pt1 > '']
    return isolist