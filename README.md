# Pomonoid
The objects defined here are an outgrowth of ad-hoc computations I needed to do while working on the article "The radical-annihilator monoid of a ring" for publication. The main objects of study are monoids which are also partially ordered sets.

In `article_examples.py`, you can find example usage of the Pomonoid class. It is possible to override generators, relations and orderings. It is also possible to create the Cartesian product of two such partially ordered monoids.

In `knumbers.py` you will find a less-developed script that was meant to explore the k- and K- numbers of a monoid directly by composing maps.

The `/img` directory contains images of the Hasse diagrams of several partially ordered monoids produced by the .draw() method. To be able to use this method yourself, you will have to install graphviz software (www.graphviz.org) and then the `graphviz` Python module (https://pypi.python.org/pypi/graphviz). 

For a long time the graphviz.org site has been unavailable (http://plantuml.sourceforge.net/qa/?qa=2773/mirror-fro-graphviz) but it is apparently still possible to find archived links to installers,  and it is possible to install with other package managers like homebrew or apt-get. The Python graphviz module can be installed with pip.
