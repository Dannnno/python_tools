import builtin


old_import = __import__

being_imported = set()

return_code = 0

def new_import(modulename, *args, **kwargs):
	if modulename in being_imported:
		print(("Importing in circles with modulename {},\n"
			   "arguments {},\n"
			   "keyword arguments {}").format(modulename, args, kwargs))
		print("    Import stack trace -> {}".format(being_imported))
		return_code = 1
	being_imported.add(modulename)
	result = old_import(modulename, *args, **kwargs)
	if modulename in being_imported:
		being_imported.remove(modulename)
	return result

__builtin__.__import__ = new_import
