# CS340_Group_Project

OSU CS340: Introduction to Databases 

Spring 2022

Group Members: Jenna Bucien, Herakles Li


Project: Penguin Library System
Project Description: This project is a fully functioning database using python flask and SQL and hosted on Heroku and JawsDB at: https://penguin-library-db.herokuapp.com/ 

Deploying to Heroku and GitHub:
https://devcenter.heroku.com/articles/git
Steps for conecting Heroku app with existing repositry for collaborative projects with Windows powershell.
1. Initalize or have local Git respository. 
2. Install Heroku CLI and login using: heroku login
3. Create a Heroku remote using: heroku create -a [APP ROOT DIRECTORY]
4. This should result in two connections, origin for github and heroku for heroku. 
5. Deploy code using: git push heroku main 
6. 