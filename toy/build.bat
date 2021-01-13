@echo off
cmd /k "cd Scripts & activate.bat & cd .. & pip install -r requirements.txt & pyinstaller -F Arithmetic_100.py -w & cd Scripts & deactivate.bat & cd .. & python zip.py"
