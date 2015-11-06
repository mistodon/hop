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