# tweets-dashboard
[![Build Status](https://travis-ci.org/divisiondeariza/tweets-dashboard.svg?branch=master)](https://travis-ci.org/divisiondeariza/tweets-dashboard)
[![Coverage Status](https://coveralls.io/repos/github/divisiondeariza/tweets-dashboard/badge.svg?branch=master)](https://coveralls.io/github/divisiondeariza/tweets-dashboard?branch=master)

Django-based Dashboard for analyzing, filtering and erasing tweets stored from api or from csv file.

It stores the data in a mysqlite database, and you can manipulate them through an admin interface powered by Django.

Currently it have some nice features as:
 - A configurable filter system
 - You can delete twets
 - A tagging system
 - A weighted-scores system.
 - Even you can select some tweets and export them in a csv!

## Getting Started
### Instalation
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
Then you can use it in http://localhost:8000/admin/tweetsDB/tweet/ with the password and username you just created.

### Populate database with your tweets
There are two ways of populate the database with your tweets, by the twitter API directly or by using the csv archive file.

#### Populating by the API
This is de easiest way of populate the database, just run:

```bash
python manage.py populate --from-api
```

And it will be update yout database automatically. This way have two inconvinients:

1. It may take a *long* time.
2. It probably will not retrieve yout oldest tweets, specially if you've been a long time in twitter

#### Populating bi the csv file

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

#### Which one use?
I recommend use the csv file method the first time you use the system, or there are tweets unreacheables by unsing the API method. Use the API method otherwise.

## Now, what can I do with this
### Filter your tweets
There are some basic ways of filtering tweets:
 - By creation date.
 - By existence (i.e. was loaded but doesn't exist in twitter anymore).
 - By if it's a tweet in response to someone or not.
 - By tags (using the tagging system)
 - By key words in tweets itselves
 
 ![Image of filter](https://raw.githubusercontent.com/divisiondeariza/tweets-dashboard/master/docs/filter.png)
 
#### Advanced Filter
It also has a system for filtering tweets in a query-styled way, which can also be combined with the other filters.

![Image of advanced filter](https://raw.githubusercontent.com/divisiondeariza/tweets-dashboard/master/docs/advanced_filter.png)

### Tag tweets
It may be useful to tag some tweets (say, in those you talk about politics set tag 'politics'), and use them as filters latter.

![Image of tags](https://raw.githubusercontent.com/divisiondeariza/tweets-dashboard/master/docs/tags.png)

### Score tweets
You can add custom scores (ratings) for different metrics to every tweet and assing a weight to each rating, and then sort them in the dashboard by the weigthed-mean of them.

![Image of rating](https://raw.githubusercontent.com/divisiondeariza/tweets-dashboard/master/docs/rating.png)

### Bulk actions
There are some actions you can do over severat tweets at the same time.

![Image of bulk actions](https://raw.githubusercontent.com/divisiondeariza/tweets-dashboard/master/docs/bulk_actions.png)

#### Delete tweets
You can bulk delete selected tweets directly from dashboard, they will be erased from twitter but remain in databased and are marked as non existent.

#### CSV export
You can select some tweets and export them in a csv file.




