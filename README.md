## TODO - A Simple Python + Flask + SQLAlchemy + SQLite3 demo web application

# Overview
This is a very simple web application I hope helps someone. My current working knowledge of Enterprise Web Applications focuses on Java EE and a little .NET. As I'm moving into Data Science/Visualization, I'm using Python a lot more. I have a couple ideas that I'd like to prototype out quickly and decided on Python. I found and recently finished this (free) Udacity course [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) to get an introduction to the popular Flask framework and SQLAlchemy ORM for Python. It's a great course and if the topics interest you, I'd highly recommend.

This is **NOT** meant to be run in a production environment. Parts of the code are commented to explain certain concepts, but it was kept very simple on purpose. This project was for me to learn and to hopefully be educational for others. It omits certain things like proper error checking, sanitizing input, having a proper data access layer, etc...

If you want to learn how to properly run Flask applications in a production environment, please see [here](http://flask.pocoo.org/docs/1.0/tutorial/deploy/)

I will also apologize in advance for the lack of appealing front end. Wanting to keep this very simple, and also working within my day to day life constraints, I had to leave it off.

# Setup
My main workstation tends to either be Linux based or macOS. For this example I used a VM with CentOS 7. All the following instructions worked for me on there, and should be very similar for other platforms (If I find time soon I'll add a Dockerfile for those interested). For this application I used Python 3.7, Anaconda (Science Platform/Python environment management), Flask, SQLAlchemy, and SQLite3. 

We start by getting Anaconda
```
sudo yum update
wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh -P ~/Downloads
```

or if that doesn't work, visit their distribution download page [Here](https://www.anaconda.com/distribution/). Next we install it

```
cd ~/Downloads
chmod +x Anaconda3-2019.03-Linux-x86_64.sh
./Anaconda3-2019.03-Linux-x86_64.sh
```

and follow the installer instructions. It will download whatever it needs, and by default install to /home/**user**/anaconda3

*NOTE: At the end it asks if you want to run conda init for your shell, type yes*

Next we need to add the path to conda, so add the following to the end of your shell configuration file (for most users with Bash that's ~/.bash_profile), then close and open a new terminal.

```
PATH=$PATH:/home/your_user_here/anaconda3/bin
export PATH
```

To test we can get a list of our currently available environments which should be *__base__* only. 

`conda info -e`

*NOTE: If you don't see it in the output, or get a conda not found error, double check above steps*

To create a new environment for the TODO application run the following

```conda create -n todo_dev python=3.7```

*NOTE: It doesn't have to be named 'todo_dev' I just did that for consistency*

We can now activate our new environment by running:

```conda activate todo_dev```

If all goes well you should see your prompt change to something similar to

```(todo_dev) [user@host]~%```

*NOTE: If you get an error/message about your shell not being initialized, simply run: conda init bash (if your shell is Bash) and open a new terminal*

We need to install a couple dependencies in our todo_dev environment, so in your terminal type the following

```
(todo_dev) [user@host]~% pip install flask
(todo_dev) [user@host]~% pip install sqlalchemy
```

*NOTE: SQLite3 was installed already, but if it's not for you simply install it now before proceeding*

Last thing to do is clone this repository to a local directory. I always keep things under ~/Source/ but it can go anywhere you'd like.

```
cd ~/Source
git clone https://github.com/fmoralesii/todo.git
```

# Run
At this point you should have everything we need in place. If you get any errors, please review the above steps again.

To run the sample application we first create the SQLite3 database file we plan on using:
```
cd ~/Source/todo
python create_db.py
```

If that goes well, then run the web application with: `python todo.py`

If it starts up ok you should see the following:
```
 * Serving Flask app "todo" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 229-624-362
```

If you now visit `http://localhost:5000/` you should see the webpage **My TODO list**

To close the development server, just press `CTRL^C` in your terminal!

If you wish to deactivate your current Anaconda environment, just type `conda deactivate`

# Code and API Notes
The TODO apps methods are all contained in `todo.py`, they support either GET or GET/POST HTTP verbs.

If the methods receive an HTTP GET request, they will render an HTML page using a predefined template (`/templates`). If they receive a POST request, they carry out the intended action and redirect to the main page. You'll notice we don't have to explicitly select the HTTP response codes, nor content type; Flask takes care of a lot of that for us.

The file `create_db.py` defines the table (class) we'll use with SQLAlchemy ORM. It is heavily commented mainly so I don't forget what each piece does.

One of the last things this course had us do is add API end points that would return JSON, so other applications could interface with us. I defined the following three end points, and sending an HTTP GET request will return JSON for other tools to use. You can either type them directly in your browser, or use your favorite RESTful API testing application; mine is [Postman](https://www.getpostman.com).

`/todo/completed/JSON`

`/todo/pending/JSON`

`/todo/<id>/JSON`

With not very many lines of Python, we have a great starting point for a web application. I think this helps illustrate just how powerful these tools and languages are.