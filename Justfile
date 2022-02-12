watch ip="127.0.0.1":
    pelican -lr content -s pelicanconf.py \
        -t ~/Projects/pelican-windows-website-2012 \
        -b {{ ip }}

publish:
    pelican content -s publishconf.py \
        -t ~/Projects/pelican-windows-website-2012 \
        -o /tmp/blog-output
    rsync -Aavx /tmp/blog-output/ www-data@avocadosh.xyz:/var/www/blog/
