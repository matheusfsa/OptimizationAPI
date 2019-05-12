from distutils.core import setup, Extension
setup(name = 'domModule', version = '1.0',  \
   ext_modules = [Extension('domModule', ['dominance.c'])])
