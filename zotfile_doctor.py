"""Checks the consistency between the zotfile-managed directory and the database"""

import sqlite3
import sys
import pathlib


def get_db_set(db):
    conn=sqlite3.connect(db)

    db_c=conn.execute('select path from itemAttachments where path like "attachments:%"')
    db_d=db_c.fetchall()

    db_l = [ x[0].replace('attachments:',"") for x in db_d]
    db_set = set(db_l)
    return db_set


def get_dir_set(d):
    p = pathlib.Path(d)
    fg = p.rglob("*.pdf")
    fs = [ str(x.relative_to(p)) for x in fg ]
    d_set = set(fs)
    return d_set

    
def main(db, d):
    db_set=get_db_set(db)
    dir_set=get_dir_set(d)

    db_not_dir = db_set.difference(dir_set)
    dir_not_db = dir_set.difference(db_set)

    print(f"There were {len(db_not_dir)} files in DB but not in zotfile directory:")
    for f in sorted(db_not_dir):
        print("   " + f)

    print("\n")
    print(f"There were {len(dir_not_db)} files in zotfile directory but not in DB:")
    for f in sorted(dir_not_db):
        print("   " + f)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} zotero.sqlite zotfile_directory")
        sys.exit(1)

    main(sys.argv[1],
         sys.argv[2])

    

    
