Hop
===
Let's you bookmark directories from your terminal and `cd` straight to them using a shorthand name.

Installation
------------
Put this repo (the hop folder) in `~/bin` and add the following line to your `.bashrc` or `.bash_profile` or whatever:

```
source ~/bin/hop/hop.sh
```

Usage
-----
Run `hop -h` to see the commands available.

### Add a bookmark

```
~$ cd path/to/folder
~/path/to/folder$ hop add folder
```

This adds a bookmark called `folder` which leads to `path/to/folder`.

### See a list of bookmarks

```
~$ hop list
folder:/usr/username/path/to/folder
```

### Hop to a folder

```
~$ hop to folder
~/path/to/folder$
```

```
~/somewhere/completely/different$ hop to folder
~/path/to/folder$
```

### Delete a bookmark

```
~$ hop remove folder
~$ hop list
~$
```