Zotfile directory consistency checker
==============================

[Zotfile](http://zotfile.com) is an extension for
[Zotero](https://www.zotero.org) reference manager software which
maintains an organized directory of literature PDF files.

This small script checks the consistency between
[Zotfile](http://zotfile.com)'s file storage and the corresponding
[Zotero](https://www.zotero.org)'s view.

It compares the annotations stored in `zotero.sqlite` file with the
PDF files in your chosen Zotfile directory. Both should be passed as
arguments. The output should be self-explanatory.  It does not modify
the files nor the zotero DB. If you want to do clean-ups, you should
do it yourself.

Requirements
------------

Python 3.5 or higher.

Usage
-----

Display differences only
```
python zotfile_doctor.py zotero.sqlite zotfile_directory
```

Display disfferences and clean zotfile directory
```
python zotfile_doctor.py zotero.sqlite zotfile_directory -c
```

Example output
--------------

```
There were 2 files in DB but not in zotfile directory:
   Statistics/Socio/Herrera et al_2010_Mapping the Evolution of Scientific Fields.PDF
   [...]

There were 8 files in zotfile directory but not in DB:
   MD/MM-PBSA/Chen et al_2016_Assessing the performance of the MM-PBSA and MM-GBSA methods.pdf
   [...]
```

See also
--------

These issues

 * https://github.com/jlegewie/zotfile/issues/96
 * https://forums.zotero.org/discussion/41179/zotfile-does-not-delete-pdf-files-when-a-database-entry-is-deleted

Known issues
------------

- Files not ending in `.pdf` will be false positives (which includes capitalized `.PDF` etc.).
- Zotero must be closed (a locked DB can't be opened).
- Current as of 9/2019. May stop working if Zotero's internal storage format changes.
- Syncing case-insensitive filesystems occasionally causes confusion (not a problem originated by this script though).

Author
------

Toni Giorgino, <www.giorginolab.it>

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
