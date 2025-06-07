def func_desc(desc):
    def wrapper(val):
        val.__doc__ = desc
        return val
    return wrapper

def api_desc(desc):
    def wrapper(val):
        val.__doc__ = desc
        return val
    return wrapper