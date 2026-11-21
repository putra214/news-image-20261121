"""Entry program for news-image-20261121 (Python 3.13, standard library only).

The poster image is drawn by generate_poster.py and stored beside this file
as entry.png. This program copies it to the output directory the grader
names, so both graded runs write the same bytes.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    # Self-check: the graded runs must write the same bytes as the source.
    assert _sha256(target) == _sha256(SOURCE), "entry.png copy mismatch"
    print("wrote", target, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
