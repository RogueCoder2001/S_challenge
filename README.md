# S_challenge

<h1>Setup Guide</h1>
How to set up and run this application

<h2>Challenge information</h2>
In this challenge, I created a backend database to track inventory for a logistics comapny. The added feature is that you can export it all to a csv or xlsx file.

<h2>Technologies Used</h2>
<li>Flask</li>
<li>Python</li>
<li>Mongodb</li>
<li>pymongo</li>

<h2>Installation</h2>
To install pymongo:(if does not work try using python3)

```
$ python -m pip install pymongo[srv]
```

To install Flask:

```
$ pip install -U Flask
```

<h2>How to Run</h2>
Clone and move into S_challenge directory, then open smd in this directory

```bash
set FLASK_APP=app
set FLASK_ENV=development
flask run
```

<h2>Using the Application</h2>
Update and delete
image
<br>
Add and export table(export table is in the exports folder under the name newnewfile.csv)
image
<br>

<h2>API testing</h2>
Test file in test folder, results are in the gif below
