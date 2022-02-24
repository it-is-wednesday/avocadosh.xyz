PELICAN := "~/.virtualenvs/avocadosh.xyz/bin/pelican"

# watch with configurable IP, to enable testing on your phone
watch ip="127.0.0.1":
    {{PELICAN}} -lr content -s pelicanconf.py -t ./theme -b {{ ip }}

publish:
    {{PELICAN}} content -s publishconf.py \
        -t ./theme \
        -o /tmp/blog-output
    rsync -Aavx /tmp/blog-output/ www-data@avocadosh.xyz:/var/www/blog/
