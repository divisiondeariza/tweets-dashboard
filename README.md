# tweets-dashboard
[![Build Status](https://travis-ci.org/divisiondeariza/tweets-dashboard.svg?branch=master)](https://travis-ci.org/divisiondeariza/tweets-dashboard)

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

Then create and update the database, and create a superuser
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

then update your API keys in the *libs/twitter_utils/secrets.py* file. To get API keys go to https://apps.twitter.com/

then start the server:

```bash
python manage.py runserver
```
Now you can use it in http://localhost:8000/admin with the password and username you just created.

## Populate database with your tweets

You can populate the database by parsing the csv file in your twitter archive (you can request it from [here](https://twitter.com/settings/account)).

```bash
python manage.py populate_from_file path/to/your/archive.csv
```

The csv from archive contains some information about all your tweets (and retweets) omits some quite interesting information like how many retweets and favourites has each tweet. You can feed the database already loaded with archive running this command:

```bash
python manage.py feed_from_api
```

By default, this only updates tweets that have not been updated before. For update favourites and retweets count for all tweets in database run:

```bash
python manage.py feed_from_api --update-all
```





