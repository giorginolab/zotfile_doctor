@echo off
python zotfile_doctor.py D:\Northword\Documents\Zotero\zotero.sqlite D:\OneDrive\Postgraduate\01_Paper
echo.
set /p flag=Does clean? please enter y/n:  
echo.
if /i %flag% == y (
	cls
	python zotfile_doctor.py D:\Northword\Documents\Zotero\zotero.sqlite D:\OneDrive\Postgraduate\01_Paper -c
	echo.
	echo DONE!
	pause>nul
)else (exit)

