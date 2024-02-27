# distutils: language = c++

cdef class DAWG:

    cdef unicode sep
    cdef dict replaces
    cdef CharType c_sep

    cdef Guide guide
    cdef Dictionary dct
    cdef Completer* completer

    def save(self, path):

        cdef ofstream stream
        path = path.encode()
        stream.open(path, binary)

        if stream.fail():
            raise IOError('save fail')

        self.dct.Write(&stream)
        self.guide.Write(&stream)
        stream.close()

    def load(self, path):

        cdef ifstream stream
        path = path.encode()
        stream.open(path, binary)

        if stream.fail():
            raise IOError('load fail')

        self.dct.Read(&stream)
        self.guide.Read(&stream)
        stream.close()

    def build(self, keys):

        keys.sort()

        cdef Dawg dawg
        cdef DawgBuilder builder

        for key in keys:
            b_key = key.encode()
            builder.Insert(b_key, len(b_key), 0)

        builder.Finish(&dawg)

        Build(dawg, &self.dct)
        Build(dawg, self.dct, &self.guide)

        dawg.Clear()


    def __init__(self, sep, replaces, keys=None, path=None):

        if path: self.load(path)
        elif keys: self.build(keys)
        else: raise ValueError('init fail')

        self.replaces = {
            k.encode(): 
            [(c.encode(), c) for c in v]
            for k, v in replaces.items()
        }

        self.completer = new Completer(self.dct, self.guide)
        self.sep, self.c_sep = sep, <unsigned int>ord(sep.encode())


    def __dealloc__(self):
        self.dct.Clear()
        self.guide.Clear()


    cdef list _similar_items(self, unicode key, unicode cur_prefix, BaseType cur_index):

        cdef int idx
        cdef list results = []
        cdef bytes b_step, b_char
        cdef unicode u_char, prefix
        cdef BaseType index = cur_index
        cdef BaseType next_index = cur_index

        for idx in range(len(cur_prefix), len(key)):

            b_step = <bytes>(key[idx].encode())

            if b_step in self.replaces: # ё
                
                for (b_char, u_char) in self.replaces[b_step]:

                    next_index = index

                    if self.dct.Follow(b_char, &next_index):
                        prefix = cur_prefix + key[len(cur_prefix):idx] + u_char
                        results.extend(self._similar_items(key, prefix, next_index))

            if not self.dct.Follow(b_step, &index): return results

        
        if self.dct.Follow(self.c_sep, &index):

            self.completer.Start(index)
            prefix = cur_prefix + key[len(cur_prefix):] + self.sep

            while self.completer.Next():
                results.append(prefix + string(self.completer.key()).decode('utf8'))

        return results


    cpdef list similar_items(self, unicode key):
        return self._similar_items(key, u'', self.dct.root())