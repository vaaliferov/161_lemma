import os, dawg, pandas as pd

from lemma.utils import load_json
from lemma.utils import dump_lines

from lemma.score import get_score
from lemma.parse import parse_dict
from lemma.merge import merge_lemmas

from lemma.split import get_stem
from lemma.split import get_prefixes
from lemma.split import get_suffixes


def split_words(group):

    words = group['word'].tolist()

    stem = get_stem(words)
    prefixes = get_prefixes(words, stem)
    suffixes = get_suffixes(words, stem)
    offsets = [len(p) for p in prefixes]

    group['prefix'] = prefixes
    group['suffix'] = suffixes
    group['stem_offset'] = offsets
    group['stem_length'] = len(stem)

    return group


def save_categories(series, path):
    cats = series.cat.categories
    dump_lines(cats.tolist(), path)


def build(dict_path, custom_dict_path, out_dir):

    data, cols = parse_dict(dict_path)
    mapping = merge_lemmas(data['links'], {7,21,23,27})

    df = pd.DataFrame(data['lemmas'], columns=cols['lemmas'])
    df['id'] = df['id'].map(mapping).fillna(df['id']).astype('uint32')

    df['tag'] = df['tag'] + ' @ ' + df['form']
    df = df.drop(columns='form')

    max_id = df['id'].max()
    custom_lemmas = load_json(custom_dict_path)

    for idx, lemma in enumerate(custom_lemmas):
        ldf = pd.DataFrame(lemma, columns=['word', 'tag'])
        df = pd.concat((df, ldf.assign(id = max_id + idx + 1)))

    df = df.reset_index(drop=True)

    df = df.groupby('id').apply(split_words, include_groups=False)
    df = df.droplevel(1).reset_index(drop=False)

    df['prefix'] = df['prefix'].astype('category')
    df['suffix'] = df['suffix'].astype('category')
    df['tag'] = df['tag'].astype('category')

    df['score'] = df['tag'].apply(get_score)
    df['norm_idx'] = df.groupby('id')['score'].transform(lambda x: x.idxmax())

    params = {
        'right_index': True,
        'left_on': 'norm_idx',
        'suffixes': ('', '_norm')
    }

    cols = ['prefix', 'suffix', 'tag']
    df = pd.merge(df, df[cols], **params)
    df = df.drop(columns='norm_idx')

    os.makedirs(out_dir, exist_ok=True)
    save_categories(df['tag'], f'{out_dir}/tags.txt')
    save_categories(df['prefix'], f'{out_dir}/prefixes.txt')
    save_categories(df['suffix'], f'{out_dir}/suffixes.txt')

    keys = df['word'].copy()
    keys += ',' + df['tag'].cat.codes.astype(str)
    keys += ',' + df['stem_offset'].astype(str)
    keys += ',' + df['stem_length'].astype(str)
    keys += ',' + df['tag_norm'].cat.codes.astype(str)
    keys += ',' + df['prefix_norm'].cat.codes.astype(str)
    keys += ',' + df['suffix_norm'].cat.codes.astype(str)

    params = {
        'sep': ',',
        'keys': keys.tolist(),
        'replaces': {'е':'ё'}
    }

    dwg = dawg.DAWG(**params)
    dwg.save(f'{out_dir}/words.dawg')