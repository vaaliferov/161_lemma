from Cython.Build import cythonize
from distutils.core import setup, Extension

setup(
    ext_modules=cythonize(Extension(
        'dawg', language='c++',
        sources=['src/lemma/dawg.pyx'],
    )),
)