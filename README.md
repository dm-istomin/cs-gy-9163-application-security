# CS-GY 9163: Application Security

This is a repository for my code from the class, Summer 2019.

## Spellchecker

A simple command-line program to spell check a text file. Should work with Python 2 or Python 3.

Usage is simple: run the program with an input file name and an output file name.
A simple input file with typos is included in this repo.

```bash
python spellchecker.py input.txt output.txt

# Produces a file called output.txt with the spelling errors corrected.
```

## Vulnerable Webapp

This is a toy web application that is very vulnerable to several attacks, built with Flask and MYSQL.
The app itself is very simple: it has two types of users, with roles like `admin` and `user`.
All normal users can do is view the page at `/users`, but admins can create new users which will show up in that list.
A couple of attacks to try against this application are listed below.

### CSRF

To perform a CSRF attack, simply login as an admin. Then open the included HTML page called
`admin_csrf_example.html`. That page will submit a POST request to create a user using the admin 
credentials without you performing an action.

### SQL Injection

This app does SQL interpolation in the wrong way, which makes it very easy to do SQL injection.
To try it out, go to the homepage login form and enter any username with this password: `' or ''='`.
It will allow you to get a session no matter what the user password is.
