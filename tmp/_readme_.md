##### Лемматизатор для русского языка

* Данная имплементация опирается на открытый корпус [opencorpora](https://www.opencorpora.org) и библиотеку [dawgdic](https://code.google.com/archive/p/dawgdic). Концептуально решение аналогично [pymorphy2](https://github.com/pymorphy2/pymorphy2). Отказ от pymorphy2 (и его форков) в пользу своей имплементации был обусловлен следующими причинами: 

    * В pymorphy2 есть проблемы с совместимостью с новыми версиями python, а также с актуальными версиями словарей opencorpora, при этом автор более не поддерживает проект. Существующие форки решают лишь часть проблем и развиваются очень медленно.

    * В pymorphy2 есть избыточный (в контексте моих проектов) функционал - склонение слов, поддержка 2 языков и т.д. Кроме того, существует потребность в функционале, который не поддерживается в pymorphy2 и существующих форках - исправление опечаток и снятие омонимии с учетом контекста, а также поддержка добавления своих лемм (специфические для компании термины и аббревиатуры + разговорные формы слов, отсутствующие в opencorpora).

* На данный момент в проекте ~300 строк кода python + ~200 строк cython (+ исходники dawgdic). При этом уже обеспечивается базовый функционал: быстрый поиск всех доступных словоформ и соответствующих им начальных форм. Скорость работы: ~150к слов / сек (один поток), расход памяти: ~11Мб (~5 млн словоформ).

##### Установка
```bash
git clone https://github.com/vaaliferov/lemma && cd lemma
python3 -m venv env && source env/bin/activate && pip install .
```

##### Загрузка словаря
```bash
wget https://opencorpora.org/files/export/dict/dict.opcorpora.xml.zip
unzip dict.opcorpora.xml.zip && rm dict.opcorpora.xml.zip
```

##### Подготовка словаря
```python
from lemma.build import build

params = {
    'out_dir': 'data',
    'dict_path': 'dict.opcorpora.xml',
    'custom_dict_path': 'dict.custom.json'
}

build(**params) # ~25min
```

##### Тестирование лемматизации
```python
from lemma.morph import Morph

morph = Morph('data')
print(*morph.search('осел'), sep='\n')
print(*morph.search('озера'), sep='\n')
print(*morph.search('винду'), sep='\n')
```