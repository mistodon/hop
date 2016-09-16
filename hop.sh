#!/bin/bash

export HOPDIR=$1

function hop() {
    result=$(python ${HOPDIR}/hop.py "$@")
    firstchar=${result:0:1}
    if [[ $firstchar == "0" ]]
    then
        newwd=${result:1}
        cd $newwd
    else
        echo "$result"
    fi
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
        shortnamesfile=~/.hop/shortnames
        touch $shortnamesfile
        bookmarks=$(cat $shortnamesfile)
        if [[ "$prev" == "to" || "$prev" == "remove" ]]
        then
            COMPREPLY=( $( compgen -W '$bookmarks' -- $cur ) )
        fi
    fi

    return 0
}

complete -F _hop_complete hop

function hopp() {
    local commandname="hop"
    local subcommand=$1
    shift

    if [ "$subcommand" == "to" ]; then
        local bookmark_name=$1
        if [ -z "$bookmark_name" ]; then
            echo "usage: $commandname $subcommand bookmark_name" 1>&2
            return 1
        fi

        local bookmarks=$(grep "${bookmark_name}:" ~/.hop/hopp_bookmarks | cut -d ":" -f 2)
        if [ -n "$bookmarks" ]; then
            cd $bookmarks
        else
            echo "hop: no bookmark found with name $bookmark_name" 1>&2
        fi
        return 0

    elif [ "$subcommand" == "add" ]; then
        local bookmark_name=$1
        if [ -z "$bookmark_name" ]; then
            echo "usage: $commandname $subcommand bookmark_name" 1>&2
            return 1
        fi
        echo "${bookmark_name}:`pwd`" >> ~/.hop/hopp_bookmarks
        return 0
        
    else
        echo "usage: $commandname <command>" 1>&2
        echo "" 1>&2
        echo "Commands:" 1>&2
        echo "  add     Add a bookmark to the current directory" 1>&2
        echo "  to      Change working directory to a bookmarked directory" 1>&2
        return 1
    fi

    return 0
}