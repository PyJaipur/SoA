# Summer of Algorithms

[![prod](https://img.shields.io/badge/prod-Production%20site-green)](https://soa.pyjaipur.org/) [![master](https://img.shields.io/badge/master-Development%20site-green)](https://pyj-soa-master.herokuapp.com)
 
PyJaipur "Summer of Algorithms" is a month-ish long program conducted during the summer months of May-June.

The aim is to have a place where people can go and learn new skills or practice existing skills and have a certificate to show for it.

## Local setup

1. Make sure you have [docker running on your machine](https://docs.docker.com/get-docker/).
2. Make sure you have [python poetry](https://python-poetry.org/) running on your machine.
3. Fork this repo and follow the steps below

```bash
git clone https://github.com/<myfork>/Summer-of-Algorithm
cd Summer-of-Algorithm
poetry install # Install dependencies
poetry shell   # Activate virtualenv
ln -s local/default/Makefile .  # Symlink
ln -s local/default/env ../env  # Symlink
make services  # Start postgres + redis servers locally
make web       # Start webserver on port 8000
```

Now you can go to http://localhost:8000 on your browser and see the development server running.

If you need to make changes to the Makefile and env file, please create a
folder in `local` and put your files there. You can then symlink to those files
instead of the default files.

## Codebase layout

This is the basic filetree for the project. Please refer to the actual filetree if this one is out of date.

```bash
├──bottle.py            # Bottle web framework to avoid pip hash issues.
├──Makefile             # Common commands and their shortcuts
├──poetry.lock
├──Procfile             # Command to run web server on heroku
├──pyproject.toml       # Project dependencies
├──README.md
├──requirements.txt     # Heroku only accepts requirements.txt. Generated using poetry export.
├──runtime.txt          # python version running on heroku
├──soa
│  ├──__init__.py
│  ├──__main__.py       # Main CLI interface `python -m soa` executes this file.
│  ├──housekeeping.py   # Code to run one time housekeeping jobs.
│  ├──mailer.py         # Handle email sending + keeps email templates.
│  ├──models.py         # Database models and functions associated with them.
│  ├──plugins.py        # Common operations performed on all web routes
│  ├──server.py         # Main server file.
│  ├──settings.py       # Contains constants which we use in the application
│  └──tracks
│     ├──__init__.py    # Used to register tracks.
│     ├──core.py        # Core functions for track management
│     ├──dsa
│     │  ├──1.md        # Each numbered Markdown file is a task in this track.
│     │  └──__init__.py # Contains track meta info
│     └──python
│        ├──1.md
│        └──__init__.py
└──views                # This folder contains html templates
   ├──account.html
   ├──alert.html
   ├──base.html
   ├──certificate.html
   ├──crumbs.html
   ├──login.html
   ├──meta.html
   ├──task.html
   └──tracks.html
```


## If you want to

- Add a new track
    - We assume the track is called 'mytrack' and has 2 tasks in it.
    - Go to `soa/tracks` and create a folder 'mytrack'
    - Create a file `soa/tracks/mytrack/__init__.py` with contents
      ```python
      from soa.tracks.core import Track

      class MyTrack(Track):
        slug = 'mytrack'
        title = 'My Track'
        description = 'Absolutely mine'
      ```
    - Create a file `soa/tracks/mytrack/1.md` and put the contents of your first task there.
    - Create a file `soa/tracks/mytrack/2.md` and put the contents of your first task there.
    - You can add forms in the task markdown files to accept user answers and mark them as done. For example:
      ```md
      ## Adding numbers

      Python lets you do mathematics. For example 1+1, and 2+2.

      How would you add 3 and 4?
      <form method='POST'>
        <input name='answer'>
        <input type='submit' value='Submit'>
        <code class='code_checker'>
        def answer(s):
            s =  s.replace(' ', '').strip()
            return s == '3+4' or s == '4+3'
        </code>
      </form>
      ```
    - Any text inside `code` tags with class `code_checker` is used to verify the correct value for the input by the same name as the function.
    - For example here, the value of the input with name `answer` will be passed to the function called `answer` that we have defined.
- Add permissions to a user
    - `echo 'user@email.com permission_string' | python -m soa --housekeeping add_perm`
- Run any housekeeping function
    - Any function defined inside the `soa.housekeeping:handle` function can be called from the command line.
    - `python -m soa --housekeeping <fn_name>`
