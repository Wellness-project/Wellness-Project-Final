# WELLNESS PROJECT

CFG GROUP PROJECT (NANODEGREE – SOFTWARE STREAM)

## About
The Wellness Web app intends to make your journaling experience more comfortable and easier, with the option for daily mood tracking and a link to external resources to help users manage their wellbeing.
The web app is designed to store user log in details, so that their journal inputs would be kept secure and visible only to them. The users are given several journaling prompts, which encourage the user to dwell on their day, practice gratitude, bring clarity and awareness to their mental wellbeing state. Once the user has completed the journal, they can submit their answers. The Daily Wellness Progress Tracker can be found under the “Mood” page and it is designed for the user to answer several questions and once submitted, this will return the user’s overall mood for the day with a score, and it will return a graph of mood scores over a period of time. The Inspirational Quote of the Day returns a motivational quote and cat pictures from APIs. And the we app contains external resources for wellbeing which may be suggested for users based on their journalling input.

# GETTING SET UP
Requirements:
[Python 3.9+](https://www.python.org/downloads/)

Required packages:                                                                                                                                                
`mysql-connector`                                                                                                                                                     
`mysql-connector-python`                                                                                                                                                
`matplotlib`                                                                                                                                                
`flask`                                                                                                                                                
`flask-sqlalchemy`                                                                                                                                                
`flask-login`                                                                                                                                                                                                                                                                                                                                                      
To install packages:                                                                                                                                                
`pip3 install mysql-connector`                                                                                                                                          
`pip3 install mysql-connector-python`                                                                                                                                   
`pip3 install matplotlib`                                                                                                                                               
`pip3 install flask`                                                                                                                                           
`pip3 install flask-sqlalchemy`                                                                                                                                      
`pip3 install flask-login`                                                                                                                                              

# HOW TO RUN
To start:
1. Open file `create_sql_script.sql` and paste and execute the code on your MySQLWorkbench                                                                                       
2. Go into `configs.py` file and insert your MySQLWorkbench `password` and `username`                                                                                       
3. Install the required packages as listed in the `“Required packages”`                                                                                            
4. The project folder `website` has to be recognised as a package due to the `__init__.py` file                                                                                    
5. Run `main.py` and open the link. Then click the link that directs you to the website
