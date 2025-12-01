#!/bin/bash

mkdir -p results
for archivo in Datos/*.txt; do
    ./main.out "$archivo"
done