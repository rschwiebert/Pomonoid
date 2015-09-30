from pomonoid import *

"""
Models of partially ordered monoids appearing in `The radical-annihilator
monoid of a ring`
"""
kura_order_relations = {('k', 'kckck'),
						('k','1'),
						('1','ckc'),
						('kckck','ckck'),
						('kckck','kckc'),
						('ckck','ckckckc'),
						('kckc','ckckckc'),
						('ckckckc','ckc'),

						('kc', 'kckckc'),
						('kc','c'),
						('c','ck'),
						('kckckc','ckckc'),
						('kckckc','kck'),
						('ckckc','ckckck'),
						('kck','ckckck'),
						('ckckck','ck'),
						}
kura = Pomonoid(base_relations={('cc', '1'), ('kk', 'k'), ('kckckck', 'kck'),
                                ('1c','c'), ('1k','k'), ('c1','c'), ('k1','k'),
                                ('11','1')},
                base_generators={'c','k'})
kura.attach_order(ordering=kura_order_relations)

kuraED = Pomonoid(base_relations={('cc', '1'), ('kk', 'k'), ('kckckck', 'kck'),
								('ckckckc', 'kckc'),
								('kckck', 'ckck'),
                                ('1c','c'), ('1k','k'), ('c1','c'), ('k1','k'),
                                ('11','1')},
                base_generators={'c','k'})
# kuraED.attach_order(ordering=kura_order_relations)

kuraEDOU = Pomonoid(base_relations={('cc', '1'), ('kk', 'k'), ('kckckck', 'kck'),
								('ckck', 'kckc'),
                                ('1c','c'), ('1k','k'), ('c1','c'), ('k1','k'),
                                ('11','1')},
                base_generators={'c','k'})

kuraOU = Pomonoid(base_relations={('cc', '1'), ('kk', 'k'), ('kckckck', 'kck'),
								('ckckckc', 'ckck'),
								('kckck', 'kckc'),
                                ('1c','c'), ('1k','k'), ('c1','c'), ('k1','k'),
                                ('11','1')},
                base_generators={'c','k'})

kuraPart = Pomonoid(base_relations={('cc', '1'), ('kk', 'k'), ('kckckck', 'kck'),
								('ckck', 'k'),
								('1c','c'), ('1k','k'), ('c1','c'), ('k1','k'),
                                ('11','1')},
                base_generators={'c','k'})

kuraDisc = Pomonoid(base_relations={('cc', '1'), ('kk', 'k'), ('kckckck', 'kck'),
								('ckc', 'k'),
                                ('1c','c'), ('1k','k'), ('c1','c'), ('k1','k'),
                                ('11','1')},
                base_generators={'c','k'})



field = Pomonoid(elements={'1', 'a'},
                 relations={('r', '1'), ('aa', '1')},
                 override_elements=True)
field.attach_order(ordering = set())

# Dual rings
dual = Pomonoid(relations={('aa', '1'), ('rara', 'rar')})
dual.attach_order(ordering={('r', '1'), ('r', 'rar'),
                            ('ra', 'rar'), ('ra', 'a'),
                            ('1', 'ara'),
                            ('a', 'ar'),
                            ('rar', 'arar'),
                            ('arar', 'ara'), ('arar', 'ar')})

largest_dual = ProductPomonoid(dual, field).export()

# Semiprime rings
semiprime = Pomonoid(relations={('ra', 'ar'), ('ar', 'a')})
semiprime.attach_order(ordering={('aa', 'r'), ('r', '1')})


# Zero dimensional local rings

ZDLRb = Pomonoid(relations={('rara', 'rar'), ('aar', 'r'), ('raa', 'r')})
ZDLRb.attach_order(ordering={
    ('r', 'aa'), ('r', 'rar'),
    ('ra', 'rar'), ('ra', 'a'),
    ('aa', 'ara'), ('aa', '1'),
    ('a', 'ar'),
    ('rar', 'arar'),
    ('arar', 'ara'), ('arar', 'ar')})

ZDLRc = Pomonoid(relations={('ara', 'ar'), ('rara', 'aar'), ('raar', 'aar')})
ZDLRc.attach_order(ordering={
                    ('aar', 'raa'), ('aar', 'ra'),
                    ('raa', 'aa'), ('raa', 'r'),
                    ('ra', 'rar'), ('ra', 'a'),
                    ('aa', '1'),
                    ('r', '1'), ('r', 'rar'),
                    ('a', 'ar'),
                    ('1', 'ar'),
                    ('rar', 'ar')})

ZDLRbf = ProductPomonoid(ZDLRb, field)
ZDLRcf = ProductPomonoid(ZDLRc, field)
ZDLRbc = ProductPomonoid(ZDLRb, ZDLRc)
# The minify() method only removes the simplest redundant paths
# The following corrections are manually removing 2-and 3-step redundancies
ZDLRbc.order.incidence[ZDLRbc.lookup['aar']][ZDLRbc.lookup['1']] = False
ZDLRbc.order.incidence[ZDLRbc.lookup['ra']][ZDLRbc.lookup['ara']] = False
ZDLRbc.order.incidence[ZDLRbc.lookup['r']][ZDLRbc.lookup['ar']] = False
#ZDLRbc.order.incidence[ZDLRbc.lookup['aarar']][ZDLRbc.lookup['ar']] = False
#ZDLRbc.order.incidence[ZDLRbc.lookup['aarar']][ZDLRbc.lookup['ara']] = False

# test4 = ProductPomonoid(ZDLRbc.export(), semiprime)
largest_zdr = ProductPomonoid(ZDLRbc.export(), field)
# largest_zdr.order.incidence[largest_zdr.lookup['aarar']][largest_zdr.lookup['ar']] = False
# largest_zdr.order.incidence[largest_zdr.lookup['aarara']][largest_zdr.lookup['ara']] = False


# semiprime.draw('semiprime')
# dual.draw('dual')
largest_dual.draw('largest_dual')
largest_zdr.draw('largest_zdr')
#
ZDLRb.draw('ZDRLb')
ZDLRc.draw('ZDRLc')
ZDLRbf.draw('ZDLRbf')
ZDLRcf.draw('ZDLRcf')
ZDLRbc.draw('ZDLRbc')
# test4.draw('test4')
trial=Pomonoid(relations={('rara','rar'),
                          ('raar', 'aar'),
                          ('araa','ar')
                          })

# need to get relations working for exported monoids to do the following
# test4 = ProductPomonoid(semiprime, ZDLRbc.export())
