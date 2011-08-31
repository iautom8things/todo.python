#################################################
#                                               #
# task_commands.py                              #
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

from task import Task
import subprocess, time, os, sys, signal, commands, constants


#######################################
#   Test that MongoDB is installed    #
#######################################

if not commands.getoutput('which mongod'):
    print "Please install MongoDB!\nSee Their Website:\thttp://mongodb.org"
    sys.exit(constants.MISSING_DEPENDANCY)

#######################################
#   Test that pymongo is installed    #
#######################################


try:
    import pymongo
except ImportError, e:
    print "Please install pymongo!"
    print "See Their Website:\thttp://pypi.python.org/pypi/pymongo/2.0.1"
    sys.exit(constants.MISSING_DEPENDANCY)


#########################
#   Global Variables    #
#########################


mongo_proc = None       # This will be the subprocess of the MongoDB server.
created = None          # Boolean statement if the subprocess was created.
db_connection = None    # The connection to the database.

kflag = "-k"            # Keywords
pflag = "-p"            # Priority


#########################
#   Helper Functions    #
#########################

def get_globalcount ( _collection ):
        """Returns the total number of created tasks.  This is used as a
        unique identifier for tasks."""

        doc = _collection.find({'global_count':{'$exists':True}}).next()
        return int(doc['global_count'])


def retrieve_collection ( ):
    """Create a connection to the MongoDB server, if it is already running,
    OR if it is not running start our own MongoDB server in a subprocess.
    Then return the collection of tasks (this is equvilent to a relational
    database's table)."""

    global created, mongo_proc, db_connection

    try:
        c = pymongo.Connection()
    except:
        with open('mongo.log', 'w') as f:   # Log the output of subprocess
            mongo_proc = subprocess.Popen('mongod', shell=True, stdout=f)
        created = True
        # mongod needs some time to setup before we try to connect to it
        time.sleep(constants.TENTH_SECOND)
        try:
            c = pymongo.Connection()
        except:
            print 'Unable to connect-to and start MongoDB.'
            print 'Are you sure Mongo is installed?'
            sys.exit(constants.SERVER_UNAVAILABLE)
    db_connection = c
    tasks = db_connection.todo.tasks

    if not tasks.find({'global_count' : {'$exists':True}}).count() > 0:
        tasks.insert({'global_count':0})

    return tasks

def destroy_connection ( ):
    """Kills the subprocess that runs the MongoDB server."""

    global mongo_proc
    os.kill(mongo_proc.pid, signal.SIGINT)

def cleanup ( ):
    """A function to cleanup the MongoDB server subprocess, if it was
    created by the script."""

    if created:
        destroy_connection()

def grab_keywords ( _args ):
    """Helper function to look for any keywords supplied by the user,
    following the keywords flag, '-k'."""

    if kflag in _args:
        k_index = _args.index(kflag)
        if pflag in _args:
            p_index = _args.index(pflag)
            if p_index > k_index:
                keywords = _args[k_index+1 : p_index]
            else:
                keywords = _args[k_index+1 : ]
        else:
            keywords = _args[k_index+1:]
    else:
        keywords = []
    return keywords

def grab_priority ( _args ):
    """Helper function to look for a priority level, if the priority flag
    '-p' is included by the user."""

    if pflag in _args:
        p_index = _args.index(pflag)
        try:
            priority = int(_args[p_index + 1])
        except:
            priority = constants.DEFAULT_PRIOTY
    else:
        priority = constants.DEFAULT_PRIOTY
    return priority


######################
#   Main Functions   #
######################


def add ( _args ):
    """
-------- Add --------

Function:

    todo add *description* [optional: *priority_level*, *keywords*]

Description:

    Creates a new task with the supplied description.
    And if supplied:
        - The priority level    # Default Value: 0  (lowest priority)
        - Keywords              # Default Value: [] (empty list)

Flags:

    -k  # Anything following this flag (up to another flag) is considered to
        # be a keyword.  You can have multiple word keywords by surrounding
        # them with quotation marks.

    -p  # A number that directly follows this flag will be the priority
        # level of the task.

Examples:

    $ todo add "call fred later" -p 10 -k foo bar baz

    ID: 1   Done: False   Task: call fred later
            Priority: 10    Keywords: ['foo', 'bar', 'baz']

    $ todo add "doctor apt" -k apt dr foot -p 100

    ID: 2   Done: False  Task: doctor apt
            Priority: 100   Keywords: ['apt', 'dr', 'foot']

    $ todo add "call for dentist apt" -k 'call dentist' apt

    ID: 3   Done: False  Task: call for dentist apt
            Priority: 0   Keywords: ['call dentist', 'apt']

    $ todo add eat

    ID: 4   Done: False Task: eat
            Priority: 0     Keywords: []
"""

    if not _args or _args[0] is kflag or _args[0] is pflag:
        print 'No description provided!'
    else:
        description = _args[0]
        _args = _args[1:]
        keywords = grab_keywords(_args)
        priority = grab_priority(_args)

        tasks = retrieve_collection()
        task_id = get_globalcount(tasks) + 1
        task = Task(task_id, description, priority, keywords)
        tasks.insert(task.__dict__)
        tasks.update({'global_count':{'$exists':True}},
                {'global_count':task_id})
        print 'Added:'
        print task
    cleanup()

def delete ( _args ):
    """
-------- Delete --------

Function:

    todo delete *task_id*

Description:

    Deletes the task associated with the given Task ID from the database,
    with NO WAY of recovering it.

Examples:

    $ todo delete 1

    Deleting...
    ID: 1   Done: True   Task: call fred later
            Priority: 10    Keywords: ['foo', 'bar', 'baz']

    $ todo delete 2

    Deleting...
    ID: 2   Done: False  Task: doctor apt
            Priority: 100   Keywords: ['apt', 'dr', 'foot']
"""

    try:
        taskid = int(_args[0])
        tasks = retrieve_collection()
        task = Task(**tasks.find({'_id' : taskid }).next())
        print 'Deleting...\n%s' % task
        tasks.remove({ '_id' : taskid })
    except ValueError:
        print "Failed."
        print "'delete' command requires an integer-based task ID."
        print "Please execute 'todo help' for further assistance."
    finally:
        cleanup()

def complete ( _args = [] ):
    """
-------- Complete --------

Function:

    todo complete *task_id*

Description:

    Marks the given task as being completed.

Examples:

    $ todo complete 8

    Completing...
    ID: 8   Done: True  Task: go to store
            Priority: 1010  Keywords: ['groceries']

    $ todo complete 7

    Completing...
    ID: 7   Done: True  Task: finish project
            Priority: 42    Keywords: ['nino', 'coding', 'python']
"""
    try:
        taskid = int(_args[0])
        tasks = retrieve_collection()
        tasks.update({'_id':taskid},{'$set':{'_completed':True}})
        task = Task(**tasks.find({'_id' : taskid }).next())
        print 'Completing...\n%s' % task
    except:
        print "Failed."
        print"'complete' command requires an integer-based task ID."
        print "Please execute 'todo help' for further assistance."
    finally:
        cleanup()

def finished ( _args = [] ):
    """
-------- Finished --------

Function:

    todo finished

Description:

    Displays a list of completed tasks, sorted in descending order with
    the most recently completed task first.

Examples:

    $ todo finished

    Finished Tasks...'

    ID: 8   Done: True  Task: go to store
            Priority: 1010  Keywords: ['groceries']
    ID: 7   Done: True  Task: finish project
            Priority: 42    Keywords: ['nino', 'coding', 'python']
"""

    tasks = retrieve_collection()
    print 'Finished Tasks...'
    for x in tasks.find({ '_completed' : True }):
        print Task(**x)
    cleanup()

def find ( _args = [] ):
    """
-------- Find --------

Function:

    todo find *keywords*

Description:

    Provided a list of keywords, return any tasks that share at least one
    of the supplied keywords.

Examples:

    $ todo find apt

    looking for ['apt']
    ID: 3   Done: False  Task: call for dentist apt
            Priority: 200   Keywords: ['dentist', 'apt']
    ID: 2   Done: False  Task: doctor apt
            Priority: 100   Keywords: ['apt', 'dr', 'foot']

    $ todo find bar apt

    looking for ['bar', 'apt']

    ID: 10  Done: True  Task: go to the
            Priority: 9000  Keywords: ['bar', 'foo', 'baz']
    ID: 3   Done: False  Task: call for dentist apt
            Priority: 200   Keywords: ['dentist', 'apt']
    ID: 2   Done: False  Task: doctor apt
            Priority: 100   Keywords: ['apt', 'dr', 'foot']
    ID: 1   Done: True   Task: call fred later
            Priority: 10    Keywords: ['foo', 'bar', 'baz']
"""
    print 'looking for %s' % _args
    tasks = retrieve_collection()
    for x in tasks.find({'_keywords' :{'$in' : _args}}):
        print Task(**x)
    cleanup()

def recent ( _args = [] ):
    """
-------- Recent --------

Functions:

    todo
    todo recent

Description:

    Displays a list of the most recently created, unfished tasks.

Examples:

    $ todo

    ID: 10  Done: False  Task: go to the
            Priority: 9000  Keywords: ['bar', 'foo', 'baz']
    ID: 3   Done: False  Task: call for dentist apt
            Priority: 200   Keywords: ['dentist', 'apt']
    ID: 2   Done: False  Task: doctor apt
            Priority: 100   Keywords: ['apt', 'dr', 'foot']
    ID: 1   Done: False   Task: call fred later
            Priority: 10    Keywords: ['foo', 'bar', 'baz']

    $ todo recent

    ID: 10  Done: False  Task: go to the
            Priority: 9000  Keywords: ['bar', 'foo', 'baz']
    ID: 3   Done: False  Task: call for dentist apt
            Priority: 200   Keywords: ['dentist', 'apt']
    ID: 2   Done: False  Task: doctor apt
            Priority: 100   Keywords: ['apt', 'dr', 'foot']
    ID: 1   Done: False   Task: call fred later
            Priority: 10    Keywords: ['foo', 'bar', 'baz']
"""
    print 'Listing most recent tasks...'
    tasks = retrieve_collection()
    count = get_globalcount(tasks)
    if not count > 0:
        print """Welcome to todo.python by Manuel Zubieta!  Execute 'todo
        help' to help get started!"""
    else:
        recent = tasks.find({'global_count':{'$exists':False},
            '_completed':False}).sort('_id' , pymongo.DESCENDING).limit(10)
        for x in recent:
            print Task(**x)
    cleanup()

def help ( _args = [] ):
    """
-------- Help --------

Function:

    todo help [optional: *command*]

Descripton:

    Display help dialogs for program/commands.

List of Commands:

    add.........Add a new task.
    delete......Delete a task.
    find........Find a task by keyword(s).
    complete....Complete a task.
    finished....List finished tasks.
    recent......List most recent unfished tasks.
    help........This help dialog.

Examples:

    $ todo help

    $ todo help add

    $ todo help find
"""
    if _args and _args[0] in commands:
        docstring = commands[_args[0]].__doc__
    else:
        docstring = help.__doc__
    print docstring

commands = {                    ############################################
    "add"       : add,          # This is a dictionary of the commands     #
    "delete"    : delete,       # for the use of parsing the input text.   #
    "complete"  : complete,     #                                          #
    "finished"  : finished,     # It must be defined at the end of the     #
    "find"      : find,         # file because it references the functions #
    "recent"    : recent,       # created earlier                          #
    "help"      : help          ############################################
}
