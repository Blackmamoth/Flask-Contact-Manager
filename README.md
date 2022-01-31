# Flask-Contact-Manager

1. Another small manager project, this is a contact manager written in Python-Flask.
2. A user needs to register and log in to the website, to create and manage contacts.
3. Once a user is logged in to the website they can create new contacts by clicking `New Contact` in the navbar.
4. After creating a contact, user will be redirected to the home page where they can see all of their contacts.
5. A User can edit/update or delete a contact from their contact list.

## To get the website running after you have clone it, you can do the following

1. Create and activate a virtual environment for Python through your command line and install the requirements for this project by typing

if on mac/linux:

`$ python3 -m venv venv_name`\
`$ source venv_name/bin/activate`\
`$ pip3 install -r requirements.txt`

if on windows:

`PS dir_name:\> python -m venv venv_name`\
`PS dir_name:\> .\venv\Scripts\activate`\
`PS dir_name:\> pip install -r requirements.txt`

2. After step 1,navigate to the root directory of the project(where **app.py** lies) to create an environment variable through command-line by typing

if on mac/linux:

`$ export FLASK_APP=app.py`

if on windows:

`PS dir_name:\> set FLASK_APP=app.py`

3. After completing the above both steps, when in the root directory of the project run this command to run the website on your localhost:

`$ flask run`

4. And then simply Navigate to **http://127.0.0.1:5000/** or **http://localhost:5000/** on your browser.
