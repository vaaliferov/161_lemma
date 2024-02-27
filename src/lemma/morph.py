import dawg
from .utils import load_lines

class Morph:

    def __init__(self, data_dir):

        params = {
            'sep': ',', 
            'replaces': {'е':'ё'},
            'path': f'{data_dir}/words.dawg'
        }

        self.dwg = dawg.DAWG(**params)
        self.tags = load_lines(f'{data_dir}/tags.txt')
        self.prefixes = load_lines(f'{data_dir}/prefixes.txt')
        self.suffixes = load_lines(f'{data_dir}/suffixes.txt')

    def parse(self, key):

        values = key.split(',')
    
        word = values[0]
        tag = self.tags[int(values[1])]
        stem_offset = int(values[2])
        stem_length = int(values[3])
    
        norm_tag = self.tags[int(values[4])]
        norm_prefix = self.prefixes[int(values[5])]
        norm_suffix = self.suffixes[int(values[6])]
    
        stem = word[stem_offset:stem_offset+stem_length]
        norm_word = norm_prefix + stem + norm_suffix
    
        return word, tag, norm_word, norm_tag

    def search(self, word):
        keys = self.dwg.similar_items(word)
        return list(map(self.parse, keys))