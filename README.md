This repository contains a module for categorizing linguistic terms into SVO categories according to WordNet classification. This module will be part of a larger package that detects and suggests variable concepts from user input.

Command line usage:

* Passing two arguments to determine whether a term has a specific category:

```
$ python ontology_category.py precipitation process
The following definitions of precipitation are process:
n. the process of forming a chemical precipitate
n. the falling to earth of any form of water (rain or snow or hail or sleet or mist)
n. the act of casting down or falling headlong from a height
n. an unexpected acceleration or hastening
```

* Passing a single argument to determine what categories a term belongs to:

```
$ python ontology_category.py precipitation
precipitation has the following categories:
n. the quantity of water falling to earth at a specific place within a specified period of time
    property
n. the process of forming a chemical precipitate
    process
n. the falling to earth of any form of water (rain or snow or hail or sleet or mist)
    object, process
n. the act of casting down or falling headlong from a height
    process
n. an unexpected acceleration or hastening
    process
n. overly eager speed (and possible carelessness)
    property
```

=======  
Please see the iPython Notebook (click this Binder link to open executable notebook in browser --> [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mariutzica/SVO-1.0.0-wn-categorization-module/960a82840f9c83678e17a4094668f84f2f2eaf05?filepath=Example%20usage%20and%20outputs.ipynb)) for a simple example of usage.

KNOWN ISSUES WITH BINDER: if you get the error

``Failed to connect to event stream``

when clicking the link and are using the Safari browser on MacOS, please switch to the Chrome browser.

