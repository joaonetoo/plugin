#!/bin/sh
# Script para varrer as notícias do uol, g1 e blasting automaticamente
cd /home/joao/plugin/venv
source bin/activate
scrapy crawl globo -o globo2.jl -s JOBDIR=globo
scrapy crawl uol -o uol2.jl -s JOBDIR=uol
scrapy crawl blasting -o blasting2.jl -s JOBDIR=blasting
python notices.py
cp uol2.jl uol.jl
cp globo2.jl globo.jl
cp blasting2.jl blasting.jl


