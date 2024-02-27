##### Lemmatizer (Russian Language)
Similarly to [pymorphy2](https://github.com/pymorphy2/pymorphy2), this implementation is based on the [opencorpora](https://www.opencorpora.org) morphological dictionary and the [dawgdic](https://code.google.com/archive/p/dawgdic) library. But, unlike pymorphy2, this version supports python 3.10+ and the latest versions of the opencorpora dictionary. In addition, this implementation has only ~300 lines of python and ~200 lines of cython code, and also only 3 dependencies: dawgdic, pandas и lxml. Performance and features: ~150K words / sec, ~11 Mb of RAM (~5M word forms), user-defined lemmas support. Future plans: contextual disambiguation and spelling correction.

##### Install
```bash
git clone https://github.com/vaaliferov/161_lemma && cd 161_lemma
python3 -m venv env && source env/bin/activate && pip install .
```

##### Download dictionary
```bash
wget https://opencorpora.org/files/export/dict/dict.opcorpora.xml.zip
unzip dict.opcorpora.xml.zip && rm dict.opcorpora.xml.zip
```

##### Build necessary files
```python
from lemma.build import build

params = {
    'out_dir': 'data',
    'dict_path': 'dict.opcorpora.xml',
    'custom_dict_path': 'dict.custom.json'
}

build(**params) # ~25min
```

##### Test lemmatization
```python
from lemma.morph import Morph

morph = Morph('data')
print(morph.search('озера'))
```
