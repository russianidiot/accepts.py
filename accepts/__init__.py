__all__ = ['accepts']

import inspect

"""
f.func_code.co_argcount  python 2.x only
"""

def _err_msg(func, args, pos, required_types):
    name = func.__name__
    lines = [
        "%s() argument #%s is not instance of %s" %
        (name, pos, required_types)]
    lines += ["args: %s" % str(list(args))]
    lines += ["arg#%s: %s" % (pos, args[pos])]
    return "\n".join(lines)


def _func_args(f):
    try:
        # getargspec() is deprecated in python3, so use drop-in-replacement getfullargspec() whenever available
        return len(inspect.getfullargspec(f).args)
    except AttributeError:
        # fall back to getargspec() if getfullargspec() is not available (python2)
        return len(inspect.getargspec(f).args)


def _validate_args(f, args, types):
    args_count = _func_args(f)
    if args_count != len(types):  # python 2.x
        msg = "%s arguments. expected: %s" % (len(types), args_count)
        raise ValueError(msg)
    for pos, (arg, required_types) in enumerate(zip(args, types), 0):
        # isinstance() arg 2 must be a type or tuple of types
        # fix: type(None)
        if not isinstance(arg, required_types):
            msg = _err_msg(f, args, pos, required_types)
            raise TypeError(msg)


def accepts(*types):
    """@accepts decorator"""
    def check_accepts(f):
        def new_f(*args, **kwargs):
            _validate_args(f, args, types)
            return f(*args, **kwargs)
        try:  # python2
            new_f.func_name = f.func_name
        except AttributeError:  # python3
            new_f.__name__ = f.__name__
        return new_f
    return check_accepts
