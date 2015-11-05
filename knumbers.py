class MapSet(object):
    def __init__(self, **kwargs):
        for funcname, mapping in kwargs.items():
            setattr(self, funcname, mapping)
        ideals = set()
        for mapping in kwargs.values():
            ideals = ideals.union(set(mapping.keys()))
            ideals = ideals.union(set(mapping.values()))
        # identity = dict(('%s' % ideal:'%s' % ideal) for ideal in ideals)
        # self.id = identity

field = MapSet(
    a = {
        'R': '0',
        '0': 'R'
    },
    r = {
        'R': 'R',
        '0': '0'
    }
)

ZDLRb = MapSet(
    r = {'0':'M',
         'I': 'M', # I is a prototypical nontrivial ideal
         'aI': 'M',
         'aaI': 'M',
         'aM': 'M',
         'M': 'M', # M is the unique maximal ideal
         'R':'R',},
    a = {'0': 'R',
         'I': 'aI',
         'aI': 'aaI',
         'aaI': 'aI',
         'M': 'aM', # aM is assumed to be nonzero, thus aaM=M
         'aM': 'M',
         'R': '0',}
)

ZDLRc = MapSet(
    r = {'0':'M',
         'I': 'M', # I is a prototypical nontrivial ideal with nonzero annihilator
         'aI': 'M',
         'aaI': 'M',
         'J': 'M', # J is a prototypical nontrivial ideal with zero annihilator
         'M': 'M', # M is the unique maximal ideal
         'R':'R',},
    a = {'0': 'R',
         'I': 'aI',
         'aI': 'aaI',
         'aaI': 'aI',
         'J':'0',
         'M': '0', # aM is assumed to be zero, thus aaM=R
         'R': '0'}
)

def compose(a, b):
    """
    Return the dict that is the composition of the two mappings.
    """
    return dict((key, a[b[key]]) for key in b.keys())

def multicompose(elt, mapset):
    seq = list(elt)
    seq = list(map(lambda x: getattr(mapset, x), seq))
    cur = seq.pop(-1)
    for item in reversed(seq):
        cur = compose(item, cur)
    return cur


def find_orbits(mapset, elements):
    allmaps = set(multicompose(elt, mapset) for elt in elements)
    for ideal in mapset.r.keys():
        print(set(f[ideal] for f in allmaps))
