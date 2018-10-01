import os
os.system("scrapy crawl globo -o globo2.jl -s JOBDIR=globo")
os.system("scrapy crawl uol -o uol2.jl -s JOBDIR=uol")
os.system("scrapy crawl blasting -o blasting2.jl -s JOBDIR=blasting")
os.system("python3 notices.py")
os.system("cp uol2.jl uol.jl")
os.system("cp globo2.jl globo.jl")
os.system("cp blasting2.jl blasting.jl")
