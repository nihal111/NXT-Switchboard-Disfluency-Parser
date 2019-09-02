#!/bin/bash
SPATH=$(pwd)
mkdir result_extracted
while IFS='' read -r line || [[ -n "$line" ]]; do
    touch "./result/$line"
    echo "extracting $line"
    python extract_all.py $line > "./result_extracted/$line"
done < "$1"
