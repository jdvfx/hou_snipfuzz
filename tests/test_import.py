from hou_snipfuzz import HouSnipFuzz
snip = HouSnipFuzz()
print(snip)

# import importlib.util
# import sys
#
#
# import tokenize
# file_path = tokenize.__file__
# module_name = tokenize.__name__
# #
# print(file_path , module_name)
#
# loc = '/home/bunker/Desktop/git/hou_snipfuzz/__init__.py'
# spec = importlib.util.spec_from_file_location("hou_snipfuzz",loc)
# if spec is not None:
#     foo = importlib.util.module_from_spec(spec)
#     if foo is not None:
#         sys.modules["module.name"] = foo
#         spec.loader.exec_module(foo)
#         print(foo.__file__)


# import sys
# sys.path.append('/home/bunker/Desktop/git/hou_snipfuzz')
# import hou_snipfuzz
# a = hou_snipfuzz.HouSnipFuzz()

        # print(


        # a = hou_snipfuzz
        # print(a)#



# a = HouSnipFuzz()
# import sys
# spec = importlib.util.spec_from_file_location("HouSn", "/path/to/file.py")
# foo = importlib.util.module_from_spec(spec)
# sys.modules["module.name"] = foo
# spec.loader.exec_module(foo)
# foo.MyClass()
#
# import sys
# sys.path.append('/home/bunker/Desktop/git')
# from hou_snipfuzz import HouSnipFuzz



# a = hou_snipfuzz.HouSnipFuzz()
# a = HouSnipFuzz()

#
#
# """
#     COPY(SAVE) SNIPPET
# """
# # a.save_hscript()
#
#
# """
#     PASTE SNIPPET
# """
# search_string = "smoke"
# search_type = hou_snipfuzz.SearchType.TAG
# matches = a.search_snippets(search_string=search_string,search_type=search_type)
#
# if matches is not None:
#     for match in matches:
#         print(f"> {match}")
#
