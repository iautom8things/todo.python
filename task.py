#################################################
#                                               #
# task.py                                       #
#                                               #
#   A simple command-line Todo List Manager     #
#                                               #
#   Dependancies:                               #
#       Python  (Developed on Version 2.7.2)    #
#       clint (Command Line INterface Tools)    #
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

from clint.textui import colored

class Task ( object ):
    """
A Task object used for validating the documents stored in MongoDB and for
defining a unified way to print a Task to screen.
"""
    def __init__ ( self, identifier, description, priority,
            keywords, completed = False ):
        """ The Constructor.  Since Tasks will be created from documents
        stored in MongoDB, we must ensure the parameter values are casted as
        the correct data type since MongoDB uses unicode strings."""

        self.identifier = int(identifier)
        self.description = str(description)
        self.priority = int(priority)
        self.keywords = map(str, keywords)
        self.completed = bool(completed)

    @property
    def _identifier ( self ):
        """Returns the Identifcation Number of the Task."""
        return self.identifier

    @property
    def _description ( self ):
        """Returns the description of the Task."""
        return self.description

    @property
    def _priority ( self ):
        """Returns the priority level of the Task."""
        return self.priority

    @property
    def _keywords ( self ):
        """Returns the keywords associated with the Task."""
        return self.keywords

    @property
    def _completed ( self ):
        """Returns whether the Task as been completed."""
        return self.completed

    @_completed.setter
    def _completed ( self, value ):
        """Sets the completed property with the value supplied."""
        if type(value) == type(True):
            self.completed = value

    def __str__ ( self ):
        """The String representation of a Task."""
        color = colored.white
        if self.priority > 100:
            color = colored.red
        elif self.priority > 50:
            color = colored.yellow
        else:
            color = colored.green

        retstring = colored.blue("Task:\n\t") + color(self.description)
        retstring += colored.blue("\nID:") + " %s\t" % self.identifier
        retstring += colored.blue("Completed: ") + "%s\t" % self.completed
        retstring += colored.blue("Priority: ") + "%s\n" % self.priority
        retstring += colored.blue("Keywords: ") + "%s" % self.keywords

        return retstring
