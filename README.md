# tweets-dashboard
Django-based Dashboard for analyzing, filtering and erasing tweets stored from api or from csv file.

It stores the data in a mysqlite database, and you can manipulate them through a

## Instalation
First, clone the repo into your local machine.

```bash
git clone https://github.com/divisiondeariza/tweets-dashboard.git
```
then install dependences. **In order to avoid collitions with your local packages, It's recomended to use a [virtual enviroment](https://virtualenv.pypa.io/en/stable/userguide/) for this**

```bash
pip install -r requirements.txt
```

Then create and update the database
```bash
python manage.py makemigrations
python manage.py migrate
```

then start the server:

```bash
python manage.py runserver
```
Now you can use it in http://localhost:8000
