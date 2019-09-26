# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Checks the consistency between the zotfile-managed directory and the database"""

import sqlite3
import sys
import unicodedata
import fnmatch
import os
import pathlib
import re

def get_db_set(db, d):
    conn = sqlite3.connect(db)

    db_c = conn.execute(
        'select path from itemAttachments where linkMode = 2 or linkMode = 3 and contentType = "application/pdf"')
    db_d = db_c.fetchall()

    db_l = []
    for i in range(len(db_d)):
        try:
            # Ignore all kind of errors wholesale, i.e. duck typing
            item = db_d[i][0]
            if not item.lower().endswith(".pdf"):
                continue
            if item.count('attachments:') > 0: # relative path
                item = item.replace('attachments:', "")
            else: # absolute path
                item = str(pathlib.Path(item).relative_to(d))
        except:
            # file is not in zotfile directory
            continue

        db_l.append(unicodedata.normalize("NFD", item))
        
    db_set = set(db_l)
    return db_set


def get_dir_set(d):
    rule = re.compile(fnmatch.translate("*.pdf"), re.IGNORECASE)
    matches = []
    for root, dirnames, filenames in os.walk(d):
        for filename in [name for name in filenames if rule.match(name)]:
            matches.append(os.path.join(root, filename))

    fs = [str(pathlib.Path(f).relative_to(d)) for f in matches]
    fs = [unicodedata.normalize("NFD", x) for x in fs]
    d_set = set(fs)
    return d_set


def main(db, d):
    db_set = get_db_set(db, d)
    dir_set = get_dir_set(d)

    db_not_dir = db_set.difference(dir_set)
    dir_not_db = dir_set.difference(db_set)

    print(
        f"There were {len(db_not_dir)}/{len(db_set)} files in DB but not in zotfile directory:")
    for f in sorted(db_not_dir):
        print("   " + f)

    print("\n")
    print(
        f"There were {len(dir_not_db)}/{len(dir_set)} files in zotfile directory but not in DB:")
    for f in sorted(dir_not_db):
        print("   " + f)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} zotero.sqlite zotfile_directory")
        sys.exit(1)

    main(sys.argv[1],
         sys.argv[2])
