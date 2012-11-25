#################################################
#                                               #
# constants.py                                  #
#                                               #
#   A simple command-line Todo List Manager     #
#                                               #
#   Dependancies:                               #
#       Python  (Developed on Version 2.7.2)    #
#                                               #
# Developed by:                                 #
#   Manuel Zubieta                              #
#   mazubieta@gmail.com                         #
#   mzubieta@uno.edu                            #
#   github.com/mazubieta                        #
#                                               #
# Developed for:                                #
#   Dr. Jaime Nino                              #
#   CSCI 4210 Software Engineering              #
#   Fall 2011 @ University of New Orleans       #
#                                               #
#################################################

import os

USER_HOME = os.environ['HOME']
TODO_HOME = os.path.join(USER_HOME, '.todo-python')
DB_PATH = os.path.join(TODO_HOME, 'tasks.db')

############
#   Time   #
############

TENTH_SECOND = .1

#######################
#   Priority Levels   #
#######################

DEFAULT_PRIORITY = 0
