# Install dependencies
pip install -r requirements.txt

# Initialize the database
python manage.py makemigrations
python manage.py migrate

# Load the data
bash scripts/data/load.sh

python manage.py runserver 0.0.0.0:8000