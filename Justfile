PYTHON := "~/.virtualenvs/avocadosh.xyz/bin/python"
PELICAN := PYTHON + " -m pelican"

# watch with configurable IP, to enable testing on your phone
watch ip="127.0.0.1":
    {{PELICAN}} -lr content -s pelicanconf.py -t ./theme -b {{ ip }}

build-collage-generator:
    cd collage && flit build

publish: clean lint build-collage-generator
    {{PELICAN}} content -s publishconf.py \
        -t ./theme \
        -o /tmp/blog-output

    rsync -Aax --delete /tmp/blog-output/ www-data@avocadosh.xyz:/var/www/avocadosh.xyz/

    scp -r ./collage/dist/*.whl www-data@avocadosh.xyz:/tmp/

    ssh www-data@avocadosh.xyz \
        '~/collage-venv/bin/pip install --upgrade /tmp/lastfm_collage_generator-*.whl'

lint:
    #!/usr/bin/fish
    # I used fish here because its expansion is actually recursive. without
    # this shebang, Just will only operate on toplevel files.
    mypy --no-color-output --python-executable {{PYTHON}} **.py

clean:
    -rm -r ./collage/dist
    -rm -r /tmp/blog-output
    -rm -r /tmp/pandoc-resume
