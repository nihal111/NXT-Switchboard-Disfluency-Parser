#!/bin/bash
SPATH=$(pwd)
mkdir result
while IFS='' read -r line || [[ -n "$line" ]]; do
    touch "./result/$line"
    echo "parsing $line"
    python parsing_all.py $line > "./result/$line"
done < "$1"
