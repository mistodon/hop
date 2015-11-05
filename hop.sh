#!/bin/bash

function hop() {
    if [[ $1 == "list" || $1 == "-h" || $1 == "" ]]
    then
        python ~/bin/hop/hop.py "$@"
    else
        path=$(python ~/bin/hop/hop.py "$@")
        cd $path
    fi
}