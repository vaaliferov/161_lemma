def get_idx(sets, id):
    for i in range(len(sets)):
        if id in sets[i]: return i

def get_mapping(sets):
    
    mapping = dict()
    
    for ids in sets:

        ids = sorted(list(ids))

        mapping.update({
            ids[i]: ids[0] 
            for i in range(1, len(ids))
        })

    return mapping

def merge_lemmas(links, excluded_types):

    sets = list()

    for ln in links:

        id, from_id, to_id, type = ln

        if type not in excluded_types:

            to_idx = get_idx(sets, to_id)
            from_idx = get_idx(sets, from_id)
    
            if to_idx == from_idx == None:
                sets.append({from_id, to_id})
    
            elif to_idx != None and from_idx == None:
                sets[to_idx].add(from_id)

            elif from_idx != None and to_idx == None:
                sets[from_idx].add(to_id)

            elif to_idx != from_idx:
                to = sets[to_idx]
                sets[from_idx].update(to)
                del sets[to_idx]

    return get_mapping(sets)