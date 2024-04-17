from hou_snipfuzz import HouSnipFuzz
from hou_snipfuzz import SearchType

snip = HouSnipFuzz()

search_string: str = "smoke"
search_type: SearchType = SearchType.TAG 

matches = snip.search_snippets(
        search_string=search_string,
        search_type=search_type
)

print(matches)
