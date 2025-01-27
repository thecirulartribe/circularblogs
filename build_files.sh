echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all deps in the venv
pip install -r requirements.txt

# collect static files using the Python interpreter from venv
python3.9 manage.py collectstatic --noinput --clear

# make migrations
python3.9 manage.py makemigrations
python3.9 manage.py migrate

echo "BUILD END"