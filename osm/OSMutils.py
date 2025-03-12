#import iso639


def omsutils_get_iso639_code ():
    """
    Returns a list of ISO 639 language codes.

    This function returns a list of language codes defined in ISO 639 standard.
    
    Returns:
        list: A list of ISO 639 language codes.
    """
    # isolist = [lg.pt1 for lg in iso639.iter_langs() if lg.pt1 > '']
    
    # fix pyinstaller with iso639 module
    isolist = ['ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn', 'bi', 'bs', 'br', 'bg', 'my', 'ca', 'ch', 'ce', 'zh', 'cu', 'cv', 'kw', 'co', 'cr', 'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fo', 'fj', 'fi', 'fr', 'ff', 'gl', 'lg', 'ka', 'de', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'is', 'io', 'ig', 'id', 'ia', 'ie', 'iu', 'ik', 'ga', 'it', 'ja', 'jv', 'kl', 'kn', 'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'kj', 'ku', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'lu', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'gv', 'mi', 'mr', 'mh', 'el', 'mn', 'na', 'nv', 'ng', 'ne', 'nd', 'se', 'no', 'nb', 'nn', 'ny', 'oc', 'oj', 'or', 'om', 'os', 'pi', 'pa', 'fa', 'pl', 'pt', 'ps', 'qu', 'ro', 'rm', 'rn', 'ru', 'sm', 'sg', 'sa', 'sc', 'gd', 'sr', 'sn', 'ii', 'sd', 'si', 'sk', 'sl', 'so', 'nr', 'st', 'es', 'su', 'sw', 'ss', 'sv', 'tl', 'ty', 'tg', 'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tn', 'tr', 'tk', 'tw', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'fy', 'wo', 'xh', 'yi', 'yo', 'za', 'zu']
    isolist.sort()
    return isolist

def square_dist (pt1, pt2):
        """
        Calculate the squared distance between two points.

        Parameters:
        pt1 (tuple): A tuple representing the coordinates of the first point (x1, y1).
        pt2 (tuple): A tuple representing the coordinates of the second point (x2, y2).

        Returns:
        float: The squared Euclidean distance between the two points.
        """
        return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)