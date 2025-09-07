@echo off
REM 
cd /d %~dp0

REM 
if exist venv\Scripts\activate (
    call venv\Scripts\activate
)

REM 
python manage.py makemigrations
python manage.py migrate

REM 
start http://127.0.0.1:8000/halls
python manage.py runserver

pause