#!/usr/bin/env python3

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

import argparse

import os
import pathlib
import re
import sqlite3
import unicodedata


def get_db_set(db, d):
    conn = sqlite3.connect(db)

    db_c = conn.execute(
        'select path from itemAttachments where linkMode = 2 or linkMode = 3 and ( contentType = "application/pdf" or contentType = "application/caj")')
    db_d = db_c.fetchall()

    db_l = []
    for i, _ in enumerate(db_d):
        try:
            # Ignore all kind of errors wholesale, i.e. duck typing
            item = db_d[i][0]
            if not item.lower().endswith(".pdf"):
                if not item.lower().endswith(".caj"):
                    continue
            if item.count('attachments:') > 0:  # relative path
                item = item.replace('attachments:', "")
            else:  # absolute path
                item = str(pathlib.Path(item).relative_to(d))
        except:
            # file is not in zotfile directory
            continue

        db_l.append(unicodedata.normalize("NFD", item))

    db_set = set(db_l)
    # print(db_l)
    return db_set


def get_dir_set(d):
    # 遍历后缀为.pdf、.caj的文件，包含子目录。两次for是为了去掉嵌套列表。https://qastack.cn/programming/4568580/python-glob-multiple-filetypes
    glob = [f for f_ in [pathlib.Path(d).glob(e) for e in ('**/*.pdf', '**/*.caj')] for f in f_]
    # print(glob)
    d_l = []
    for i in glob:
        i = pathlib.Path(i).relative_to(d)   # 转换为相对链接
        i = pathlib.Path.as_posix(i)         # windows-->unix
        # print(i)
        d_l.append(i)
    # print(d_l)
    d_set = set(d_l)
    return d_set




def remove_empty_dirs(d):
    for root, dirnames, _filenames in os.walk(d, topdown=False):
        for dirname in dirnames:
            try:
                os.rmdir(os.path.realpath(os.path.join(root, dirname)))
            except OSError:
                continue


def main(db, d, clean=False):
    db_set = get_db_set(db, d)
    dir_set = get_dir_set(d)

    db_not_dir = db_set.difference(dir_set)
    dir_not_db = dir_set.difference(db_set)

    print(f"There were {len(db_not_dir)}/{len(db_set)} files in DB but not in zotfile directory:")
    for f in sorted(db_not_dir):
        print("   " + f)
    print(f"\nThere were {len(dir_not_db)}/{len(dir_set)} files in zotfile directory but not in DB:")
    for f in sorted(dir_not_db):
        print("   " + f)

    if clean and len(dir_not_db) > 0:
        for f in dir_not_db:
            os.remove(os.path.join(d, f))
        remove_empty_dirs(d)
        print(f"\n{len(dir_not_db)} files and empty directories has been removed")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="zotfile directory consistency checker")
    parser.add_argument("zotero_sqlite", help="path-to-zotero/zotero.sqlite")
    parser.add_argument("zotfile_directory", help="zotfile directory")
    parser.add_argument("-c", "--clean", action="store_true",
                        help="remove files in zotfile directory but not in DB")
    args = parser.parse_args()
    main(args.zotero_sqlite, args.zotfile_directory, args.clean)
    '''
    db = "D:/Northword/Documents/Zotero/zotero.sqlite"
    d = "D:/OneDrive/Postgraduate/01_Paper"
    main(db, d, False)
    '''
