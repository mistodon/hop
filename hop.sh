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