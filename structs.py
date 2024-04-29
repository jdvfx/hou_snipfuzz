from dataclasses import dataclass

@dataclass
class SearchMatch:
    pattern:str
    source_string:str
    found_string:str
    match_score:float

@dataclass
class SearchType:
    fuzzy:bool
    ignorecase:bool

def search(pattern:str,source_string:str,search_type:SearchType)-> SearchMatch | None:

    if search_type.ignorecase:
        pattern = pattern.lower()
        source_string = source_string.lower()

    if search_type.fuzzy:
        print("fuzzy search")
    else:
        if pattern not in source_string:
            return None
        return SearchMatch(
            pattern=pattern,
            source_string=source_string,
            found_string=pattern,
            match_score=1.0
        )

    s = SearchMatch(
        pattern="bob",
        source_string="gog",
        found_string="kewr",
        match_score=123.123
    )
    return s


