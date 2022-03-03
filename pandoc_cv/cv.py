#!/usr/bin/env python3

from pathlib import Path
from shutil import copy

from sh import Command

TMP_DIR = "/tmp/pandoc-resume"
STYLE = "chmduquesne"

pandoc = Command("pandoc")
mtxrun = Command("mtxrun")


def pdf(input_file: Path, dest: Path, styles_dir: Path):
    """
    Create a pdf file at dest
    """
    pandoc(
        input_file,
        standalone=True,
        template=f"{styles_dir}/{STYLE}.tex",
        read="org",  # from
        to="context",
        variable="papersize=A4",
        output=f"{TMP_DIR}/{input_file.stem}.tex",
    )

    mtxrun(
        f"{input_file.stem}.tex",
        path=TMP_DIR,
        result=f"{input_file.stem}.pdf",
        script="context",
        _out=f"{TMP_DIR}/context.log",
        _long_sep=" ",
    )

    copy(f"{TMP_DIR}/{input_file.stem}.pdf", dest)


def html(input_file: Path, dest: Path, styles_dir):
    """
    Create an HTML file at dest
    """
    pandoc(
        input_file,
        standalone=True,
        include_in_header=f"{styles_dir}/{STYLE}.css",
        lua_filter=f"{styles_dir}/pdc-links-target-blank.lua",
        read="org",
        to="html",
        metadata=f'pagetitle="{input_file.stem}"',
        output=dest,
    )


def docx(input_file: Path, dest: Path):
    """
    Create a DOCX file at dest
    """
    pandoc(
        input_file,
        standalone=True,
        output=dest,
    )


def already_generated(title: str, out_dir_path: str):
    out_dir = Path(out_dir_path)
    files_to_find = [f"{title}.{ext}" for ext in ["pdf", "html", "docx"]]
    for f in files_to_find:
        if not out_dir.joinpath(f).exists():
            return False
    return True


def generate_all(input_file: Path, out_dir: Path, styles_dir: Path):
    out_dir.mkdir(exist_ok=True)
    Path(TMP_DIR).mkdir(exist_ok=True)

    title = input_file.stem

    print("\nGenerating CV:")

    pdf(input_file, out_dir.joinpath(f"{title}.pdf"), styles_dir)
    print("  ✔ PDF")

    html(input_file, out_dir.joinpath(f"{title}.html"), styles_dir)
    print("  ✔ HTML")

    docx(input_file, out_dir.joinpath(f"{title}.docx"))
    print("  ✔ DOCX")
