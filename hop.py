import argparse
import os
import json


def get_bookmark_file_path(file_path="~/.hop/bookmarks.json"):
    apath = os.path.abspath(os.path.expanduser(file_path))
    dirs, fname = os.path.split(apath)
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    if not os.path.exists(apath):
        with open(apath, "w") as f:
            json.dump({}, f)
    return apath

def load_bookmarks():
    apath = get_bookmark_file_path()
    with open(apath, "r") as infile:
        bookmarks = json.load(infile)
    return bookmarks

def save_bookmarks(bookmarks):
    apath = get_bookmark_file_path()
    with open(apath, "w") as outfile:
        json.dump(bookmarks, outfile, sort_keys=True)

def hop_to(args):
    bookmarks = load_bookmarks()
    path = bookmarks.get(args.bookmark_name)
    if path:
        print(path)

def hop_add(args):
    bookmarks = load_bookmarks()
    path = os.getcwd()
    bookmarks[args.bookmark_name] = path
    save_bookmarks(bookmarks)
    print(".")

def hop_remove(args):
    bookmarks = load_bookmarks()
    path = os.getcwd()
    bookmarks.pop(args.bookmark_name)
    save_bookmarks(bookmarks)
    print(".")

def hop_list(args):
    bookmarks = load_bookmarks()
    bookmark_list = sorted(bookmarks.items())
    for bookmark, path in bookmark_list:
        print("{0} --> {1}".format(bookmark, path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hop to a bookmarked directory")
    subparsers = parser.add_subparsers()

    to_command = subparsers.add_parser("to", help="hop to a bookmark")
    to_command.add_argument("bookmark_name", type=str,
        help="the bookmark to hop to")
    to_command.set_defaults(func=hop_to)

    add_command = subparsers.add_parser("add", help="add a bookmark")
    add_command.add_argument("bookmark_name", type=str,
        help="the name to bookmark the current directory under")
    add_command.set_defaults(func=hop_add)

    remove_command = subparsers.add_parser("remove", help="remove a bookmark")
    remove_command.add_argument("bookmark_name", type=str,
        help="the name of the bookmark to remove")
    remove_command.set_defaults(func=hop_remove)

    list_command = subparsers.add_parser("list", help="list all bookmarks")
    list_command.set_defaults(func=hop_list)

    args = parser.parse_args()
    args.func(args)