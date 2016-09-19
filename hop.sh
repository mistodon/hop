#!/bin/bash

export HOPDIR=$1

function hop() {
    local commandname="hop"
    local subcommand=$1
    local usage_string="usage: hop [-h] command"
    shift

    if [ "$subcommand" == "to" ]; then
        _hop_to "$@"
        return $?

    elif [ "$subcommand" == "add" ]; then
        _hop_add "$@"
        return $?

    elif [ "$subcommand" == "remove" ]; then
        _hop_remove "$@"
        return $?

    elif [ "$subcommand" == "list" ]; then
        _hop_list "$@"
        return $?
        
    elif [ "$subcommand" == "-h" -o "$subcommand" == "--help" ]; then
        echo "$usage_string"
        echo ""
        echo "Commands:"
        echo "  add     Add a bookmark to the current directory"
        echo "  remove  Remove a bookmark by name"
        echo "  to      Change working directory to a bookmarked directory"
        echo "  list    List all available bookmarks"
        return 0
    fi
    echo "$usage_string" 1>&2  
    return 1
}

function _hop_complete() {
    local cur

    all_commands="to add remove list"

    COMPREPLY=()
    cur=${COMP_WORDS[COMP_CWORD]}
    prev=${COMP_WORDS[COMP_CWORD-1]}

    if [[ COMP_CWORD -eq 1 ]]
    then
        COMPREPLY=( $( compgen -W '$all_commands' -- $cur ) )
    elif [[ COMP_CWORD -eq 2 ]]
    then
        bookmarks=$(_hop__get_shortnames)
        if [[ "$prev" == "to" || "$prev" == "remove" ]]
        then
            COMPREPLY=( $( compgen -W '$bookmarks' -- $cur ) )
        fi
    fi

    return 0
}

complete -F _hop_complete hop

function _hop_list() {
    if [ "$1" == "-h" -o "$1" == "--help" ]; then
        echo "usage: hop list [-h]"
        echo "List all bookmarks"
    else
        cat ~/.hop/hopp_bookmarks
    fi
    return $?
}

function _hop__get_bookmark() {
    _hop_list | grep "^$1:" | cut -d ":" -f 2
}

function _hop__get_shortnames() {
    _hop_list | grep -oh "^[^:]*" | tr '\n' ' '
}

function _hop_add() {
    local usage_string="usage: hop add [-h] bookmark_name"
    local bookmark_name=$1
    if [ -z "$bookmark_name" ]; then
        echo "$usage_string" 1>&2
        return 1
    elif [ "$bookmark_name" == "-h" -o "$bookmark_name" == "--help" ]; then
        echo "$usage_string"
        echo "Add a bookmark with the given name pointing to the current directory"
        return 0
    fi
    local bookmarks=$(_hop__get_bookmark ${bookmark_name})
    if [ -n "$bookmarks" ]; then
        echo "hop: bookmark '$bookmark_name' already exists" 1>&2
        return 1
    fi
    echo "${bookmark_name}:`pwd`" >> ~/.hop/hopp_bookmarks
    return 0
}

function _hop_remove() {
    local usage_string="usage: hop remove [-h] bookmark_name"
    local bookmark_name=$1
    if [ -z "$bookmark_name" ]; then
        echo "$usage_string" 1>&2
        return 1
    elif [ "$bookmark_name" == "-h" -o "$bookmark_name" == "--help" ]; then
        echo "$usage_string"
        echo "Remove the bookmark with the given name"
        return 0
    fi
    sed "/^${bookmark_name}:/ d" ~/.hop/hopp_bookmarks > ~/.hop/hopp_bookmarks_backup
    if [ $? -ne 0 ]; then
        rm ~/.hop/hopp_bookmarks_backup
        return 1
    fi
    mv ~/.hop/hopp_bookmarks_backup ~/.hop/hopp_bookmarks
    return 0
}

function _hop_to() {
    local usage_string="usage: hop to [-h] bookmark_name"
    local bookmark_name=$1
    if [ -z "$bookmark_name" ]; then
        echo "$usage_string" 1>&2
        return 1
    elif [ "$bookmark_name" == "-h" -o "$bookmark_name" == "--help" ]; then
        echo "$usage_string"
        echo "Change working directory to the location of a bookmark with the given name"
        return 0
    fi
    local bookmarks=$(_hop__get_bookmark ${bookmark_name})
    if [ -n "$bookmarks" ]; then
        cd "$bookmarks"
        return $?
    fi
    echo "hop: no bookmark found with name $bookmark_name" 1>&2
    return 1
}

alias reload="source ~/.profile"