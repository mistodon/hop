Hop
===
Bookmarking directories for your terminal.

Installation
------------
Put this repo (the hop folder) in `~/bin` and add the following line to your `.bashrc` or `.bash_profile` or whatever:

```
. ~/bin/hop/hop.sh ~/bin/hop
```

If you put it somewhere else, change the paths in the above line to point to that directory.

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
total 1
folder --> /usr/username/path/to/folder
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
total 0

```