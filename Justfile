PYTHON := "~/.virtualenvs/avocadosh.xyz/bin/python"
PELICAN := PYTHON + " -m pelican"

# watch with configurable IP, to enable testing on your phone
watch ip="127.0.0.1":
    {{PELICAN}} -lr content -s pelicanconf.py -t ./theme -b {{ ip }}

publish:
    {{PELICAN}} content -s publishconf.py \
        -t ./theme \
        -o /tmp/blog-output
    rsync -Aavx /tmp/blog-output/ www-data@avocadosh.xyz:/var/www/avocadosh.xyz/

lint:
    #!/usr/bin/fish
    # I used fish here because its expansion is actually recursive. without
    # this shebang, Just will only operate on toplevel files.
    mypy --no-color-output --python-executable {{PYTHON}} **.py
