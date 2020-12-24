= Gifter - A MontyHub Project =

The purpose of this project is track payments, shares and other benefits for 
MontyHub members.

== INSTALLATION ==

General requirements:

* python3
* pip3
* linux or similar

pip3 -r install requirements.txt

== QUICKSTART ==

Run "./run.sh" to start up a development service on http://localhost:5000 

In development mode you will be able to login simply by specifying a username 
(no password required). In production mode we will use SAML to log into google 
workspace using the montyhub.org account

== HACKING ==

This project is built on python and based around two or three main components:

* Flask   -- Does the backend web stuff                            
	-- https://flask.palletsprojects.com/en/1.1.x/
* PonyORM -- This is what handles the database and database models 
	-- https://ponyorm.org/
* JQuery  -- Javascript library for all the frontend interactive stuff
	-- https://jquery.com/

=== PROJECT STRUCTURE ===

    requirements.txt -- pip3 modules needed to run the project
    run.py           -- python file to start dev server
    run.sh           -- shell script to start dev server (RUN THIS)
    gifter/ main app folder
       app.py -- this is where the main app web controller is defined (flask)
       share.py -- object representing shares in montyhub based on rational
                   numbers
       config.py -- create config depending on if prod mode or not
       db/ -- database stuff (pony)
          models/ -- database models (pony)
       templates/ -- html templates for web, used Jinja2 template language
       static/    -- static files for web
          style.css -- css file
          script.js -- main javascript file (jquery)

=== DATABASE MODEL ===

* ActionLog  -- All actions taken by admins are recorded in this append only log
* AdminUser  -- an administrator
* PublicUser -- a member of the public. These are the people that make payments.
                If an admin makes payments they should also have a PublicUser
* Payment    -- A payment


The basic idea is that all actions are recorded and will be available for all 
admins to see in the interests of transparency. If you make a mistake, the 
initial mistake is recorded, and then also the action rectifying it. 


