from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "<iostream>" namespace "std":
    cdef cppclass istream: 
        istream() except +
    cdef cppclass ostream: 
        ostream() except +

cdef extern from "<fstream>" namespace "std":
    cdef cppclass ifstream(istream):
        void open(char* filename, int mode) except +
        ifstream& read(char* s, int n) except +
        void close() except +
        bool fail() except +
    cdef cppclass ofstream(ostream):
        void open(char* filename, int mode) except +
        ofstream& write(char* s, int n) except +
        void close() except +
        bool fail() except +

cdef extern from "<iostream>" namespace "std::ios_base":
    int binary

cdef extern from "../../lib/dawgdic/src/dawgdic/base-types.h" namespace "dawgdic":
    ctypedef int SizeType
    ctypedef int ValueType
    ctypedef char CharType
    ctypedef unsigned int BaseType
    ctypedef unsigned char UCharType

cdef extern from "../../lib/dawgdic/src/dawgdic/guide.h" namespace "dawgdic":
    cdef cppclass Guide:
        void Clear() nogil
        bint Read(istream *input) except + nogil
        bint Write(ostream *output) except + nogil

cdef extern from "../../lib/dawgdic/src/dawgdic/dictionary.h" namespace "dawgdic":
    cdef cppclass Dictionary:
        void Clear() nogil
        BaseType root() nogil
        bint Read(istream *input) except + nogil
        bint Write(ostream *output) except + nogil
        bint Follow(CharType *s, BaseType *index) nogil
        bint Follow(CharType label, BaseType *index) nogil

cdef extern from "../../lib/dawgdic/src/dawgdic/completer.h" namespace "dawgdic":
    cdef cppclass Completer:
        char *key() nogil
        bint Next() nogil
        void Start(BaseType index) nogil
        Completer(Dictionary &dic, Guide &guide)

cdef extern from "../../lib/dawgdic/src/dawgdic/dawg.h" namespace "dawgdic":
    cdef cppclass Dawg:
        void Clear() nogil

cdef extern from "../../lib/dawgdic/src/dawgdic/dawg-builder.h" namespace "dawgdic":
    cdef cppclass DawgBuilder:
        bint Finish(Dawg *dawg)
        bint Insert(CharType *key, SizeType length, ValueType value)

cdef extern from "../../lib/dawgdic/src/dawgdic/guide-builder.h" namespace "dawgdic::GuideBuilder":
    cdef bint Build(Dawg &dawg, Dictionary &dic, Guide* guide)

cdef extern from "../../lib/dawgdic/src/dawgdic/dictionary-builder.h" namespace "dawgdic::DictionaryBuilder":
    cdef bint Build(Dawg &dawg, Dictionary *dic)