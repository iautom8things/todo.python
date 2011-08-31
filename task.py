#################################################
#                                               #
# task.py                                       #
#                                               #
#   A simple command-line Todo List Manager     #
#                                               #
#   Dependancies:                               #
#       MongoDB (Developed on Version 1.8.2)    #
#       Python  (Developed on Version 2.7.2)    #
#       PyMongo (Developed on Version 1.11)     #
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

class Task ( object ):
    """
A Task object used for validating the documents stored in MongoDB and for
defining a unified way to print a Task to screen.
"""
    def __init__ ( self, _id, _description, _priority,
            _keywords, _completed = False ):
        """ The Constructor.  Since Tasks will be created from documents
        stored in MongoDB, we must ensure the parameter values are casted as
        the correct data type since MongoDB uses unicode strings."""

        self._id = int(_id)
        self._description = str(_description)
        self._priority = int(_priority)
        self._keywords = map(str, _keywords)
        self._completed = bool(_completed)

    @property
    def id ( self ):
        """Returns the Identifcation Number of the Task."""
        return self._id

    @property
    def description ( self ):
        """Returns the description of the Task."""
        return self._description

    @property
    def priority ( self ):
        """Returns the priority level of the Task."""
        return self._priority

    @property
    def keywords ( self ):
        """Returns the keywords associated with the Task."""
        return self._keywords

    @property
    def completed ( self ):
        """Returns whether the Task as been completed."""
        return self._completed

    @completed.setter
    def completed ( self, value ):
        """Sets the completed property with the value supplied."""
        if type(value) == type(True):
            self._completed = value

    def __str__ ( self ):
        """The String representation of a Task."""
        return """ID: %s\tDone:%s\tTask: %s
        Priority: %s\tKeywords: %s""" % (self._id, self._completed,
                self._description, self._priority, self._keywords)
