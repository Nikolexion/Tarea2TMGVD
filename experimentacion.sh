#!/bin/bash

mkdir -p results
for archivo in Datos/*.txt; do
    ./main "$archivo"
done