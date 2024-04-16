
import sys
#import importlib

sys.path.append('/home/bunker/Desktop/git')
import hou_snipfuzz

a = hou_snipfuzz.HouSnipFuzz()



"""
    COPY(SAVE) SNIPPET
"""
# a.save_hscript()


"""
    PASTE SNIPPET
"""
search_string = "smoke"
search_type = hou_snipfuzz.SearchType.TAG
matches = a.search_snippets(search_string=search_string,search_type=search_type)

if matches is not None:
    for match in matches:
        print(f"> {match}")

