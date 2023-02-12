echo " BUILD STARTED "
python3.9 -m venv env
source env/bin/activate
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
echo " BUILD ENDED "