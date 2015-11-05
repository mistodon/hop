#!/bin/bash

function hop() {
    result=$(python ~/bin/hop/hop.py "$@")
    firstchar=${result:0:1}
    if [[ $firstchar == "0" ]]
    then
        newwd=${result:1}
        cd $newwd
    else
        echo "$result"
    fi
}