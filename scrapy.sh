#!/bin/sh
# Script para varrer as notícias do uol, g1 e blasting automaticamente
scrapy crawl globo -o globo.jl -s JOBDIR=globo
scrapy crawl uol -o uol.jl -s JOBDIR=uol
scrapy crawl blasting -o blasting.jl -s JOBDIR=blasting



