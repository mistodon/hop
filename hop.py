import argparse
import os
import json


CHANGE_DIRECTORY_CODE = "0"


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
        print(CHANGE_DIRECTORY_CODE + path)
    else:
        print("No bookmark found named '{0}'".format(args.bookmark_name))

def hop_add(args):
    bookmarks = load_bookmarks()
    path = os.getcwd()
    bookmarks[args.bookmark_name] = path
    save_bookmarks(bookmarks)
    print(CHANGE_DIRECTORY_CODE + ".")

def hop_remove(args):
    bookmarks = load_bookmarks()
    path = os.getcwd()
    bookmarks.pop(args.bookmark_name)
    save_bookmarks(bookmarks)
    print(CHANGE_DIRECTORY_CODE + ".")

def hop_list(args):
    search = args.search_term
    match_case = args.case_sensitive
    name_only = args.name_only
    path_only = args.path_only
    bookmarks = load_bookmarks()
    bookmark_list = sorted(bookmarks.items())
    filtered = [item for item in bookmark_list
                if in_search(item[0], item[1], search, match_case, name_only, path_only)]
    print("total {0}".format(len(filtered)))
    for bookmark, path in filtered:
        print("{0} --> {1}".format(bookmark, path))

def in_search(bookmark, path, search, match_case, name_only, path_only):
        if not match_case:
            (search, bookmark, path) = (s.lower() for s in (search, bookmark, path))
        in_name = search in bookmark and not path_only
        in_path = search in path and not name_only
        return in_name or in_path


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
    list_command.add_argument("search_term", type=str, default="", nargs="?",
        help="show only bookmarks containing this term")
    list_command.add_argument("-c", "--case-sensitive", action="store_true",
        help="match case in search results")
    list_command.add_argument("-n", "--name-only", action="store_true",
        help="search bookmark names only")
    list_command.add_argument("-p", "--path-only", action="store_true",
        help="search bookmark paths only")
    list_command.set_defaults(func=hop_list)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()