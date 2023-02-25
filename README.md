# academy-project
IT Academy graduation Python project
This is a web app for small education services helping management of students students' academic performance.


Dependencies:

-Python 3.11

-Poetry


Installation:

-download this repository

-in this repository via cmd run:
"poetry install",
"poetry run python manage.py migrate",
"poetry run python manage.py createsuperuser"
"poetry run python manage.py runserver"

-enjoy


Details:

-there are three types of users:
student, teacher, director.

-Student may see their own grades and classrooms

-Teacher may see any classroom and commit new lessons in their own ones.

-Director may see any classroom and commit changes in them, delete and create new ones; Create, view, delete and edit users and their permissions.

-By default any user when is signed up gains role of student. When user account is created by director any role is allowed.
