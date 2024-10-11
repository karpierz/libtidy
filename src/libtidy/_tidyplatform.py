# **************************************************************************** #
# @file
# Platform specific definitions, specifics, and headers. This file is
# included by `tidy.h` already, and need not be included separately. Among
# other things, the PLATFORM_NAME is defined and the most common systems
# headers are included.
#
# @note It should be largely unnecessary to modify this file unless adding
# support for a completely new architecture. Most options defined in this
# file specify defaults that can be overridden by the build system; for
# example, passing -D flags to CMake.
#
# @author  Charles Reitzel [creitzel@rcn.com]
# @author  HTACG, et al (consult git log)
#
# @copyright
#     Copyright (c) 1998-2017 World Wide Web Consortium (Massachusetts
#     Institute of Technology, European Research Consortium for Informatics
#     and Mathematics, Keio University).
# @copyright
#     See tidy.h for license.
#
# @date      Created 2001-05-20 by Charles Reitzel
# @date      Updated 2002-07-01 by Charles Reitzel
# @date      Further modifications: consult git log.
# **************************************************************************** #

import ctypes as ct

from ._platform import defined

# =============================================================================
# Unix console application features
#   By default on Unix-like systems when building for the console program,
#   support runtime configuration files in /etc/ and in ~/. To prevent this,
#   set ENABLE_CONFIG_FILES to NO. Specify -DTIDY_CONFIG_FILE and/or
#   -DTIDY_USER_CONFIG_FILE to override the default paths in tidyplatform.h.
# @note: this section refactored to support #584.
#===========================================================================*/

# #define ENABLE_CONFIG_FILES

#if defined(TIDY_ENABLE_CONFIG_FILES)
#  if !defined(TIDY_CONFIG_FILE)
#    define TIDY_CONFIG_FILE "/etc/tidy.conf"
#  endif
#  if !defined(TIDY_USER_CONFIG_FILE)
#    define TIDY_USER_CONFIG_FILE "~/.tidyrc"
#  endif
#else
#  if defined(TIDY_CONFIG_FILE)
#    undef TIDY_CONFIG_FILE
#  endif
#  if defined(TIDY_USER_CONFIG_FILE)
#    undef TIDY_USER_CONFIG_FILE
#  endif
#endif

# =============================================================================
# Unix tilde expansion support
#   By default on Unix-like systems when building for the console program,
#   this flag is set so that Tidy knows getpwname() is available. It allows
#   tidy to find files named ~your/foo for use in the HTML_TIDY environment
#   variable or TIDY_CONFIG_FILE or TIDY_USER_CONFIG_FILE or on the command
#   command line: -config ~joebob/tidy.cfg
# Contributed by Todd Lewis.
# =============================================================================

# #define SUPPORT_GETPWNAM

# =============================================================================
# Optional Tidy features support
# =============================================================================

# Enable/disable support for additional languages
#ifndef SUPPORT_LOCALIZATIONS
#  define SUPPORT_LOCALIZATIONS 1
#endif
    
# Enable/disable support for console
#ifndef SUPPORT_CONSOLE_APP
#  define SUPPORT_CONSOLE_APP 1
#endif

# =============================================================================
# Platform specific convenience definitions
# =============================================================================

# === Convenience defines for Mac platforms ===

#if defined(macintosh)
# Mac OS 6.x/7.x/8.x/9.x, with or without CarbonLib - MPW or Metrowerks 68K/PPC compilers
#  define MAC_OS_CLASSIC
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Mac OS"
#  endif

# needed for access()
#  if !defined(_POSIX) && !defined(NO_ACCESS_SUPPORT)
#    define NO_ACCESS_SUPPORT
#  endif

#  ifdef SUPPORT_GETPWNAM
#    undef SUPPORT_GETPWNAM
#  endif

#elif defined(__APPLE__) && defined(__MACH__)
    # Mac OS X (client) 10.x (or server 1.x/10.x) - gcc or Metrowerks MachO compilers
#  define MAC_OS_X
#  ifndef PLATFORM_NAME
#    include "TargetConditionals.h"
#    if TARGET_OS_IOS
#      define PLATFORM_NAME "Apple iOS"
#    elif TARGET_OS_MAC
#      define PLATFORM_NAME "Apple macOS"
#    elif TARGET_OS_TV
#      define PLATFORM_NAME "Apple tvOS"
#    elif TARGET_OS_WATCH
#      define PLATFORM_NAME "Apple watchOS"
#    else
#      define PLATFORM_NAME "Apple Unknown OS"
#    endif
#  endif
#endif

#if defined(MAC_OS_CLASSIC) || defined(MAC_OS_X)
# Any OS on Mac platform
#  define MAC_OS
#  FILENAMES_CASE_SENSITIVE = False
#endif

# === Convenience defines for BSD-like platforms ===

#if defined(__FreeBSD__)
#  define BSD_BASED_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "FreeBSD"
#  endif

#elif defined(__NetBSD__)
#  define BSD_BASED_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "NetBSD"
#  endif

#elif defined(__OpenBSD__)
#  define BSD_BASED_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "OpenBSD"
#  endif

#elif defined(__DragonFly__)
#  define BSD_BASED_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "DragonFly"
#  endif

#elif defined(__MINT__)
#  define BSD_BASED_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "FreeMiNT"
#  endif

#elif defined(__bsdi__)
#  define BSD_BASED_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "BSD/OS"
#  endif
#endif

# === Convenience defines for Windows platforms ===

#if defined(WINDOWS) || defined(_WIN32)

#  define WINDOWS_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Windows"
#  endif

#  if defined(__MWERKS__) || defined(__MSL__)
     # not available with Metrowerks Standard Library
#    ifdef SUPPORT_GETPWNAM
#      undef SUPPORT_GETPWNAM
#    endif
     # needed for setmode()
#    if !defined(NO_SETMODE_SUPPORT)
#      define NO_SETMODE_SUPPORT
#    endif
#  endif

#  FILENAMES_CASE_SENSITIVE = False
#  define SUPPORT_POSIX_MAPPED_FILES 0

#endif # WINDOWS #

# === Convenience defines for Linux platforms ===

#if defined(linux) && defined(__alpha__)
   # Linux on Alpha - gcc compiler
#  define LINUX_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Linux/Alpha"
#  endif

#elif defined(linux) && defined(__sparc__)
    # Linux on Sparc - gcc compiler
#  define LINUX_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Linux/Sparc"
#  endif

#elif defined(linux) && (defined(__i386__) || defined(__i486__) || defined(__i586__) || defined(__i686__))
    # Linux on x86 - gcc compiler
#  define LINUX_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Linux/x86"
#  endif

#elif defined(linux) && defined(__powerpc__)
    # Linux on PPC - gcc compiler
#  define LINUX_OS
#  if defined(__linux__) && defined(__powerpc__)
#    ifndef PLATFORM_NAME
       # MkLinux on PPC  - gcc (egcs) compiler
#      define PLATFORM_NAME "MkLinux"
#    endif
#  else
#    ifndef PLATFORM_NAME
#      define PLATFORM_NAME "Linux/PPC"
#    endif
#  endif

#elif defined(linux) || defined(__linux__)
    # generic Linux
#  define LINUX_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Linux"
#  endif
#endif

# === Convenience defines for Solaris platforms ===
 
#if defined(sun)
#  define SOLARIS_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Solaris"
#  endif
#endif

# === Convenience defines for HPUX + gcc platforms ===

#if defined(__hpux)
#  define HPUX_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "HPUX"
#  endif
#endif

# === Convenience defines for RISCOS + gcc platforms ===

#if defined(__riscos__)
#  define RISC_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "RISC OS"
#  endif
#endif

# === Convenience defines for OS/2 + icc/gcc platforms ===

#if defined(__OS2__) || defined(__EMX__)
#  define OS2_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "OS/2"
#  endif
#  FILENAMES_CASE_SENSITIVE = False
#endif

# === Convenience defines for IRIX ===

#if defined(__sgi)
#  define IRIX_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "SGI IRIX"
#  endif
#endif

# === Convenience defines for AIX ===

#if defined(_AIX)
#  define AIX_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "IBM AIX"
#  endif
#endif

# === Convenience defines for BeOS platforms ===

#if defined(__BEOS__)
#  define BE_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "BeOS"
#  endif
#endif

# === Convenience defines for Haiku platforms ===

#if defined(__HAIKU__)
#  define HAIKU
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Haiku"
#  endif
#endif

# === Convenience defines for Cygwin platforms ===

#if defined(__CYGWIN__)
#  define CYGWIN_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "Cygwin"
#  endif
#  FILENAMES_CASE_SENSITIVE = False
#endif

# === Convenience defines for OpenVMS ===

#if defined(__VMS)
#  define OPENVMS_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "OpenVMS"
#  endif
#  FILENAMES_CASE_SENSITIVE = False
#endif

# === Convenience defines for DEC Alpha OSF + gcc platforms ===

#if defined(__osf__)
#  define OSF_OS
#  ifndef PLATFORM_NAME
#    define PLATFORM_NAME "DEC Alpha OSF"
#  endif
#endif

# === Convenience defines for ARM platforms ===

#if defined(__arm)
#  define ARM_OS
#  if defined(forARM) && defined(__NEWTON_H)
     # Using Newton C++ Tools ARMCpp compiler
#    define NEWTON_OS
#    ifndef PLATFORM_NAME
#      define PLATFORM_NAME "Newton"
#    endif
#  else
#    ifndef PLATFORM_NAME
#      define PLATFORM_NAME "ARM"
#    endif
#  endif
#endif

# =============================================================================
# Standard Library Includes
# =============================================================================

#ifdef SUPPORT_GETPWNAM
#  include <pwd.h>
#endif

# =============================================================================
# Case sensitive file systems
# =============================================================================

# By default, use case-sensitive filename comparison.
#if not defined("FILENAMES_CASE_SENSITIVE"):
#  FILENAMES_CASE_SENSITIVE = True
#endif

# =============================================================================
# Last modified time preservation
#   Tidy preserves the last modified time for the files it cleans up.
#
#   If your platform doesn't support <utime.h> and the utime() function, or
#   <sys/futime> and the futime() function then set PRESERVE_FILE_TIMES to 0.
#
#   If your platform doesn't support <sys/utime.h> and the futime() function,
#   then set HAS_FUTIME to 0.
#
#   If your platform supports <utime.h> and the utime() function requires the
#   file to be closed first, then set UTIME_NEEDS_CLOSED_FILE to 1.
# =============================================================================

# Keep old PRESERVEFILETIMES define for compatibility
#ifdef PRESERVEFILETIMES
#  undef PRESERVE_FILE_TIMES
#  define PRESERVE_FILE_TIMES PRESERVEFILETIMES
#endif

#ifndef PRESERVE_FILE_TIMES
#  if defined(RISC_OS) || defined(OPENVMS_OS) || defined(OSF_OS)
#    define PRESERVE_FILE_TIMES 0
#  else
#    define PRESERVE_FILE_TIMES 1
#  endif
#endif

#if PRESERVE_FILE_TIMES

#  ifndef HAS_FUTIME
#    if defined(CYGWIN_OS) || defined(BE_OS) || defined(OS2_OS) || defined(HPUX_OS) || defined(SOLARIS_OS) || defined(LINUX_OS) || defined(BSD_BASED_OS) || defined(MAC_OS) || defined(__MSL__) || defined(IRIX_OS) || defined(AIX_OS) || defined(__BORLANDC__) || defined(__GLIBC__) || defined(__HAIKU__)
#      define HAS_FUTIME 0
#    else
#      define HAS_FUTIME 1
#    endif
#  endif

#  ifndef UTIME_NEEDS_CLOSED_FILE
#    if defined(SOLARIS_OS) || defined(BSD_BASED_OS) || defined(MAC_OS) || defined(__MSL__) || defined(LINUX_OS)
#      define UTIME_NEEDS_CLOSED_FILE 1
#    else
#      define UTIME_NEEDS_CLOSED_FILE 0
#    endif
#  endif

#  if defined(MAC_OS_X) || (!defined(MAC_OS_CLASSIC) && !defined(__MSL__))
#    include <sys/types.h>
#    include <sys/stat.h>
#  else
#    include <stat.h>
#  endif

#  if HAS_FUTIME
#    include <sys/utime.h>
#  else
#    include <utime.h>
#  endif

# MS Windows needs _ prefix for Unix file functions.
# Not required by Metrowerks Standard Library (MSL).
#
# Tidy uses following for preserving the last modified time.
#
# WINDOWS automatically set by Win16 compilers.
# _WIN32 automatically set by Win32 compilers.
 
#  if defined(_WIN32) && !defined(__MSL__) && !defined(__BORLANDC__)
#    define futime _futime
#    define fstat _fstat
#    define utimbuf _utimbuf  # Windows seems to want utimbuf
#    define stat _stat
#    define utime _utime
#    define vsnprintf _vsnprintf
#  endif

#endif

# =============================================================================
# Windows file functions
# Windows needs _ prefix for Unix file functions.
# Not required by Metrowerks Standard Library (MSL).
#
# WINDOWS automatically set by Win16 compilers.
# _WIN32 automatically set by Win32 compilers.
# =============================================================================

#if defined(_WIN32) && !defined(__MSL__) && !defined(__BORLANDC__)

#  if !(defined(__WATCOMC__) || defined(__MINGW32__))
#    define fileno _fileno
#    define setmode _setmode
#  endif

#  if defined(_MSC_VER)
#    define fileno _fileno
#    if !defined(NDEBUG) && !defined(ENABLE_DEBUG_LOG) && !defined(DISABLE_DEBUG_LOG)
#      define ENABLE_DEBUG_LOG
#    endif
#  endif

#endif # _WIN32 #

#if defined(_WIN32)

#  ifndef TIDY_THREAD_LOCAL
#    ifdef _MSC_VER
#      define TIDY_THREAD_LOCAL __declspec( thread )
#    endif
#  endif

#endif # _WIN32 #

# =============================================================================
# Other definitions
# =============================================================================

#ifndef TIDY_THREAD_LOCAL
#  define TIDY_THREAD_LOCAL __thread
#endif

#ifndef TIDY_INDENTATION_LIMIT
#  define TIDY_INDENTATION_LIMIT 50
#endif

byte    = ct.c_ubyte
tchar   = ct.c_uint    # uint      # single, full character
tmbchar = ct.c_char    # ct.c_char # single, possibly partial character
tmbstr  = ct.c_char_p  # tmbchar * # pointer to buffer of possibly partial chars
ctmbstr = ct.c_char_p  # tmbchar const * # Ditto, but const
NULLSTR = ct.c_char_p(b"")

#ifndef SUPPORT_POSIX_MAPPED_FILES
#  define SUPPORT_POSIX_MAPPED_FILES 1
#endif

# `bool` is a reserved word in some but not all C++ compilers depending on age.
# age. Work around is to avoid bool by introducing a new enum called `Bool`.
    
# We could use the C99 definition where supported
# typedef _Bool Bool;
# #define no (_Bool)0
# #define yes (_Bool)1

#typedef enum
#{
no  = False
yes = True
#} Bool;

# for NULL pointers 
# #define null ((const void*)0)
# extern ct.c_void_p null;

#if defined(DMALLOC)
#  include "dmalloc.h"
#endif

# Opaque data structure.
# Cast to implementation type struct within lib.
# This will reduce inter-dependencies/conflicts w/ application code.
#

# Opaque data structure used to pass back
# and forth to keep current position in a
# list or other collection.
#
class _TidyIterator(ct.Structure): pass #{ int _opaque; }
TidyIterator = ct.POINTER(_TidyIterator)

del defined

# eof
