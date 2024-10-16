# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: HTMLTIDY

import sys
import os
import platform
import ctypes as ct

is_windows = (bool(platform.win32_ver()[0])
              or (sys.platform in ("win32", "cygwin", "msys"))
              or (sys.platform == "cli" and os.name in ("nt", "ce"))
              or (os.name == "java"
                  and "windows" in platform.java_ver()[3][0].lower()))
is_linux   = sys.platform.startswith("linux")
is_macos   = (sys.platform == "darwin")
is_android = hasattr(sys, "getandroidapilevel")
is_posix   = (os.name == "posix")
is_32bit   = (sys.maxsize <= 2**32)

def defined(varname, __getframe=sys._getframe):
    frame = __getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals

def from_oid(oid, __cast=ct.cast, __py_object=ct.py_object):
    return __cast(oid, __py_object).value if oid else None

del sys, os, platform, ct

if is_windows:
    from ._windows import DLL_PATH, DLL, dlclose, CFUNC
    from ._windows import time_t, timeval
elif is_linux:
    from ._linux   import DLL_PATH, DLL, dlclose, CFUNC
    from ._linux   import time_t, timeval
elif is_macos:
    from ._macos   import DLL_PATH, DLL, dlclose, CFUNC
    from ._macos   import time_t, timeval
else:
    raise ImportError("unsupported platform")
