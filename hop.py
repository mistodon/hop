import argparse
import os
import json


CHANGE_DIRECTORY_CODE = "0"


def ensure_directory(path):
    apath = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(apath):
        os.makedirs(apath)
    return apath

def get_bookmark_file_path(file_path="~/.hop/bookmarks.json"):
    dirs, fname = os.path.split(file_path)
    dirpath = ensure_directory(dirs)
    apath = os.path.join(dirpath, fname)
    if not os.path.exists(apath):
        with open(apath, "w") as f:
            json.dump({}, f)
    return apath

def get_short_names_file_path(file_path="~/.hop/shortnames"):
    dirs, fname = os.path.split(file_path)
    dirpath = ensure_directory(dirs)
    apath = os.path.join(dirpath, fname)
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
    shortfile = get_short_names_file_path()
    with open(shortfile, "w") as outfile:
        outfile.write(" ".join(bookmarks.keys()))

def hop_to(bookmarks, args):
    splitpath = args.bookmark_name.split("/", 1)
    bookmark = splitpath[0]
    relative = splitpath[1] if len(splitpath) > 1 else ""
    path = bookmarks.get(bookmark)
    if path:
        fullpath = correct_path(path, relative)
        return (True, fullpath)
    else:
        return (False, "No bookmark found named '{0}'".format(bookmark))

def hop_add(bookmarks, args):
    bookmark_name = args.bookmark_name
    if "/" in bookmark_name:
        return (False, "Error: bookmark names cannot contain '/'")
    path = os.getcwd()
    bookmarks[bookmark_name] = path
    return (False, "Added bookmark: {0}".format(show_bookmark(args.bookmark_name, path)))

def hop_remove(bookmarks, args):
    path = os.getcwd()
    bookmarks.pop(args.bookmark_name)
    return (False, "Removed bookmark: {0}".format(show_bookmark(args.bookmark_name, path)))

def hop_list(bookmarks, args):
    search = args.search_term
    match_case = args.case_sensitive
    name_only = args.name_only or args.short
    path_only = args.path_only
    bookmark_list = sorted(bookmarks.items())
    filtered = [item for item in bookmark_list
                if in_search(item[0], item[1], search, match_case, name_only, path_only)]
    if args.short:
        report = " ".join(name for name, path in filtered)
    else:
        report = "total {0}\n".format(len(filtered))
        report += "\n".join(show_bookmark(bookmark, path) for bookmark, path in filtered)
    return (False, report)

def correct_path(root, relative_path):
    if not relative_path:
        return root
    path = root
    segments = [s for s in os.path.split(relative_path) if s]
    while segments:
        seg = segments.pop(0)
        choices = next(os.walk(path))[1]
        best = best_match(seg, choices)
        path = os.path.join(path, best)
    return path

def best_match(string, candidates):
    return sorted(score_candidates(string, candidates))[0][1]

def score_candidates(string, candidates):
    # This is lame, do it better
    for candidate in candidates:
        score = 10
        if candidate == string:
            score = 0
        elif candidate.startswith(string):
            score = 1
        elif candidate.endswith(string):
            score = 2
        elif string in candidate:
            score = 3
        elif string[0] == candidate[0]:
            score = 4
        yield (score, candidate)


def show_bookmark(bookmark, path):
    return "{0} --> {1}".format(bookmark, path)

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
    list_command.add_argument("-s", "--short", action="store_true",
        help="show a short list of bookmarks")
    list_command.add_argument("-n", "--name-only", action="store_true",
        help="search bookmark names only")
    list_command.add_argument("-p", "--path-only", action="store_true",
        help="search bookmark paths only")
    list_command.set_defaults(func=hop_list)

    args = parser.parse_args()
    if "func" in args:
        bookmarks = load_bookmarks()
        change_dir, stdout_text = args.func(bookmarks, args)
        save_bookmarks(bookmarks)
        if change_dir:
            print(CHANGE_DIRECTORY_CODE + stdout_text)
        else:
            print(stdout_text)
    else:
        parser.print_help()