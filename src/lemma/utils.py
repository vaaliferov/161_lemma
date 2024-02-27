import json

def load_lines(path):
    with open(path) as fd:
        return fd.read().split('\n')

def dump_lines(lines, path):
    with open(path, 'w') as fd:
        fd.write('\n'.join(lines))

def load_json(path):
    with open(path) as fd:
        return json.load(fd)

def dump_json(obj, path):
    with open(path, 'w') as fd:
        json.dump(obj, fd, ensure_ascii=False)