import copy
import itertools
from collections import namedtuple

# Base classes


class Operation(object):
    generators = {'a', 'r'}

    def __init__(self, relations=set(), override_table=dict()):

        self.table = override_table
        self.relations = {('aaa', 'a'), ('rr', 'r'), ('11', '1'),
                          ('1a', 'a'), ('a1', 'a'),
                          ('1r', 'r'), ('r1', 'r')}.union(relations)

    def reduce(self, word):
        """
        :param word: word (string) to be reduced
        :return: reduced word (string) according to relations
        """

        orig = copy.copy(word)
        for x, y in self.relations:
            if x in word:
                word = word.replace(x, y)
        if word == orig:
            return word
        else:
            return self.reduce(word)

    def prod(self, x, y):
        """
        A binary operation. The operation can be overridden by subclasses, but
        it should always return a reduced result.
        :param x: input
        :param y: input
        :return: product of inputs, same type as inputs
        """
        return self.reduce(x + y)

    def _generate_table(self, elements):
        """
        :param elements: set of elements of the Monoid
        :return: None (table is established in Operation object)
        """
        self.table = dict((x, dict((y, self.prod(x, y))
                          for y in elements))
                          for x in elements)


class Order(object):
    def __init__(self, order_relations=set(), elements=set(),
                 override_ordering=dict(),
                 override_incidence=dict()):
        if not override_ordering:
            self.pairs = order_relations
            self.elements = elements
            self.ordering = dict((e, dict((f, False) for f in self.elements))
                                 for e in self.elements)
            self.incidence = dict((e, dict((f, False) for f in self.elements))
                                  for e in self.elements)

            for x, y in self.pairs:
                self.ordering[x][y] = True
                self.incidence[x][y] = True

            self._minify()
            self._maxify()
        else:
            self.ordering = override_ordering
            self.incidence = override_incidence

    def incidence_sum(self):
        c = 0
        for a, b in itertools.product(self.elements, self.elements):
            if self.incidence[a][b] is True:
                c += 1
        return c

    def _minify(self):
        i = 0
        while i < 10000:
            count1 = self.incidence_sum()
            for a, b, c in itertools.product(self.elements,
                                             self.elements,
                                             self.elements):
                if len({a, b, c}) < 3:
                    pass
                if self.incidence[a][b] and self.incidence[b][c]:
                    self.incidence[a][c] = False
            count2 = self.incidence_sum()
            if count2 == count1:
                break
            i += 1
        return self.incidence

    def _maxify(self):
        i = 0
        while i < 10000:
            count1 = self.incidence_sum()
            for a, b, c in itertools.product(self.elements,
                                             self.elements,
                                             self.elements):
                if len({a, b, c}) < 3:
                    pass
                if self.ordering[a][b] and self.ordering[b][c]:
                    self.ordering[a][c] = True
            count2 = self.incidence_sum()
            if count2 == count1:
                break
            else:
                i += 1
        return self.ordering

    def compare(self, x, y):
        """
        Report if x >= y

        :param x, y: elements
        :return: Boolean
        """
        return (self.ordering[x][y] is True) or (x == y)

    def report_incidence(self):
        for k in self.incidence:
            print(k)
            for j in self.incidence[k]:
                if self.incidence[k][j]:
                    print('\t', j)


class ProductElement(object):
    def __init__(self, original, left, right):
        self.original = original
        self.left = left
        self.right = right

    @property
    def pair(self):
        return (self.left, self.right)

    def __str__(self):
        return str(self.original)

    def __repr__(self):
        """
        Make it hashable so it can be used for keys in the tables.
        """
        return str((self.original, self.left, self.right))

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.left == other.left and \
            self.right == other.right


class ProductOrder(Order):
    def __init__(self, M, N, elements):
        self.order1 = M.order
        self.order2 = N.order
        self.elements = elements
        self.ordering = dict((e, dict((f, False) for f in self.elements))
                             for e in self.elements)
        self._maxify()
        self.incidence = copy.deepcopy(self.ordering)
        self._minify()

    def compare(self, x, y):
        return self.order1.compare(x.left, y.left) and \
            self.order2.compare(x.right, y.right)

    def incidence_sum(self):
        c = 0

        for a, b in itertools.product(self.elements, self.elements):
            if self.incidence[a][b] is True:
                c += 1
        return c

    def _maxify(self):
        for x, y in itertools.product(self.elements, self.elements):
            if self.compare(x, y):
                self.ordering[x][y] = True
        # make ordering dictionary strict
        for x in self.elements:
            self.ordering[x][x] = False

    def _minify(self):
        i = 0
        while i < 10000:
            count1 = self.incidence_sum()
            for x, y, z in itertools.product(self.elements,
                                             self.elements, self.elements):
                if self.incidence[x][y] and self.incidence[y][z]:
                    self.incidence[x][z] = False
            count2 = self.incidence_sum()
            if count1 == count2:
                break
            else:
                i += 1


class ProductOperation(Operation):
    def __init__(self, M, N):
        self.basic_operation = Operation()
        self.operation1 = M.operation
        self.operation2 = N.operation
        self.relations = set()

    def reduce(self, element):
        return ProductElement(self.basic_operation.reduce(element.original),
                              self.operation1.reduce(element.left),
                              self.operation2.reduce(element.right))

    def prod(self, x, y):
        """
        Operation in the product monoid
        """
        return (self.basic_operation.reduce(x.original+y.original),
                self.operation1.prod(x.left, y.left),
                self.operation2.prod(x.right, y.right))


class Pomonoid(object):
    def __init__(self, elements=set(), relations=set(),
                 ordering=set(),
                 is_export=False,
                 override_elements=False,
                 override_table=dict(),
                 override_ordering=dict(),
                 override_incidence=dict()):

        if not is_export:
            self.operation = Operation(relations=relations)
            if override_elements:
                self.elements = elements
            else:
                self.elements = elements.union({'1', 'a', 'r'})

            self._generate_elements()
            self.operation._generate_table(self.elements)
            self.order = Order(ordering, self.elements)
        else:
            self.elements = override_elements
            self.operation = Operation(relations=relations,
                                       override_table=override_table)
            self.order = Order(override_incidence=override_incidence,
                               override_ordering=override_ordering)


    def _generate_elements(self):
        self.elements = {'1'}
        n = 1
        while n < 1000:
            start = len(self.elements)
            self.elements = self.elements.union(
                self._generate_n_words(n))
            if len(self.elements) > start:
                n += 1
            else:
                break

    def _generate_n_words(self, n):
        """
        :param n: integer length of words to be generated
        :return: Set of elements resulting after reduction
        """
        result = set()
        for combination in itertools.product(*[self.operation.generators]*n):
            new_elt = ''.join(combination)
            result.add(self.operation.reduce(new_elt))
        return result

    def draw(self, file):
        import graphviz as gv
        gr = gv.Digraph(format='png')
        for e in self.elements:
            gr.node("%s" % e)
        for e, f in itertools.product(self.elements, self.elements):
            if self.order.incidence[e][f]:
                gr.edge("%s" % e, "%s" % f)
        gr.render('img/%s' % file)


class ProductPomonoid(Pomonoid):
    def __init__(self, M1, M2):
        self.M1 = M1
        self.M2 = M2
        self.relation_tracker = {'1':set(), 'a':set()}
        self.elements = set()
        self.operation = ProductOperation(self.M1, self.M2)
        self._generate_elements()
        self.operation._generate_table(self.elements)
        self.order = ProductOrder(self.M1, self.M2, self.elements)
        self.lookup = dict((e.original, e) for e in self.elements)


    @property
    def pairs(self):
        return set((e.left, e.right) for e in self.elements)

    def _generate_elements(self):
        self.elements = {ProductElement('1', '1', '1')}
        n = 1
        while n < 1000:
            start = len(self.elements)
            self._generate_n_words(n)
            if len(self.elements) > start:
                n += 1
            else:
                break

    def _generate_n_words(self, n):
        """
        :param n: integer length of words to be generated
        :return: Set of elements resulting after reduction
        """
        result = set()
        for combination in itertools.product(*[self.operation.generators]*n):
            seq = ''.join(combination)
            new_elt = self.operation.reduce(ProductElement(seq, seq, seq))
            if new_elt.pair not in self.pairs:
                self.elements.add(new_elt)
                self.relation_tracker[new_elt.original] = set()
            else:
                for e in self.elements:
                    if e.pair == new_elt.pair:
                        old_elt = e
                if old_elt.original != new_elt.original:
                    self.relation_tracker[old_elt.original].add(new_elt.original)
                    pair = (old_elt.__str__(), new_elt.__str__())
                    pair = tuple(sorted(pair, key=len, reverse=True))
                    self.operation.relations.add(pair)

    def export(self):
        elements = set(x.original for x in self.elements)
        table = dict((x.original, dict((y.original, self.operation.table[x][y])
                     for y in self.operation.table[x]))
                     for x in self.operation.table)
        incidence = dict(
            (x.original, dict((y.original, self.order.incidence[x][y])
                              for y in self.order.incidence[x]))
            for x in self.order.incidence)
        ordering = dict(
            (x.original, dict((y.original, self.order.ordering[x][y])
                              for y in self.order.ordering[x]))
            for x in self.order.ordering)
        relations = set()
        for k in self.relation_tracker:
            for item in self.relation_tracker[k]:
                if len(item) >= len(k):
                    relations.add((item, k))

        return Pomonoid(relations=relations,
                        override_table=table,
                        override_elements=elements,
                        override_incidence=incidence,
                        override_ordering=ordering,
                        is_export=True)

dual = Pomonoid(relations={('aa', '1'), ('rara', 'rar')},
                ordering={
                    ('r', '1'), ('r', 'rar'),
                    ('ra', 'rar'), ('ra', 'a'),
                    ('1', 'ara'),
                    ('a', 'ar'),
                    ('rar', 'arar'),
                    ('arar', 'ara'), ('arar', 'ar')})

semiprime = Pomonoid(relations={('ra', 'ar'), ('ar', 'a')},
                     ordering={('aa', 'r'), ('r', '1')})

field = Pomonoid(ordering = set(),
                 elements={'1', 'a'},
                 relations={('r', '1'), ('aa', '1')},
                 override_elements=True)

ZDRb = Pomonoid(relations={('rara', 'rar'), ('aar', 'r'), ('raa', 'r')},
                ordering={
                    ('r', 'aa'), ('r', 'rar'),
                    ('ra', 'rar'), ('ra', 'a'),
                    ('aa', 'ara'), ('aa', '1'),
                    ('a', 'ar'),
                    ('rar', 'arar'),
                    ('arar', 'ara'), ('arar', 'ar')})

ZDRc = Pomonoid(relations={('ara', 'ar'), ('rara', 'aar'), ('raar', 'aar')},
                ordering={
                    ('aar', 'raa'), ('aar', 'ra'),
                    ('raa', 'aa'), ('raa', 'r'),
                    ('ra', 'rar'), ('ra', 'a'),
                    ('aa', '1'),
                    ('r', '1'), ('r', 'rar'),
                    ('a', 'ar'),
                    ('1', 'ar'),
                    ('rar', 'ar')})

# field is a collapse of semiprime
# dual is a collapse of ZDRb monoid

test1 = ProductPomonoid(ZDRb, field)
test2 = ProductPomonoid(ZDRc, field)
test3 = ProductPomonoid(ZDRb, ZDRc)
# The minify() method only removes the simplest redundant paths
# The following corrections are manually removing 2-and 3-step redundancies
test3.order.incidence[test3.lookup['aar']][test3.lookup['1']] = False
test3.order.incidence[test3.lookup['ra']][test3.lookup['ara']] = False
test3.order.incidence[test3.lookup['r']][test3.lookup['ar']] = False
#test3.order.incidence[test3.lookup['aarar']][test3.lookup['ar']] = False
#test3.order.incidence[test3.lookup['aarar']][test3.lookup['ara']] = False

# test4 = ProductPomonoid(test3.export(), semiprime)
largest_dual = ProductPomonoid(dual, field)
largest_zdr = ProductPomonoid(test3.export(), field)
largest_zdr.order.incidence[largest_zdr.lookup['aarar']][largest_zdr.lookup['ar']] = False
# largest_zdr.order.incidence[largest_zdr.lookup['aarara']][largest_zdr.lookup['ara']] = False


# semiprime.draw('semiprime')
# dual.draw('dual')
largest_dual.draw('largest_dual')
largest_zdr.draw('largest_zdr')
#
ZDRb.draw('ZDRb')
ZDRc.draw('ZDRc')
test1.draw('test1')
test2.draw('test2')
test3.draw('test3')
# test4.draw('test4')
trial=Pomonoid(relations={('rara','rar'),
                          ('raar', 'aar'),
                          ('araa','ar')
                          })

# need to get relations working for exported monoids to do the following
# test4 = ProductPomonoid(semiprime, test3.export())
