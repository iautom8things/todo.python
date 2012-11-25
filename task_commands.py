#################################################
#                                               #
# task_commands.py                              #
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
import sys
import sqlite3
import constants
from task import Task


#############################################
#   Test that TODO_HOME directory exists    #
#############################################

if not os.path.exists(constants.TODO_HOME):
    os.makedirs(constants.TODO_HOME)
    try:
        assert(os.path.isdir(constants.TODO_HOME))
    except AssertionError:
        print "We were unable to create our home directory (%s). " % constants.TODO_HOME,
        print "Maybe a file exists with a similar name, or you ",
        print "do not have the proper permissions."
        sys.exit(1)


createDB = not os.path.exists(constants.DB_PATH)
db_connection = sqlite3.connect(constants.DB_PATH)
db_cursor = db_connection.cursor()

if createDB:
    db_cursor.execute("""CREATE TABLE tasks
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             description TEXT,
                             priority INTEGER,
                             completed INTEGER);""")
    db_cursor.execute("""CREATE TABLE keywords
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             task_id INTEGER,
                             keyword TEXT,
                             FOREIGN KEY(task_id) REFERENCES tasks(id));""")

def add_task_to_db ( description, priority ):
    db_cursor.execute("""INSERT INTO tasks
            (description,priority,completed) VALUES (?,?,?);""", (description,priority,False))
    db_cursor.execute("SELECT last_insert_rowid();")
    task_id = db_cursor.fetchone()[0]
    return task_id

def add_keyword_to_db ( task_id, keyword ):
    db_cursor.execute("""INSERT INTO keywords (task_id,keyword) VALUES (?,?);""", (task_id,keyword))

def get_task_by_id ( task_id ):
    db_cursor.execute("SELECT * FROM tasks WHERE id=?;",(task_id,))
    task_id, description, priority, completed = db_cursor.fetchone()
    db_cursor.execute("SELECT keyword FROM keywords WHERE task_id=?;",(task_id,))
    keywords = [ x[0] for x in db_cursor.fetchall() ]
    return Task(task_id,description,priority,keywords,completed)

def get_list_of_completed_tasks ( ):
    db_cursor.execute("SELECT id FROM tasks WHERE completed=?;",(True,))
    return [ x[0] for x in db_cursor.fetchall() ]

def get_list_of_uncompleted_tasks ( ):
    db_cursor.execute("SELECT id FROM tasks WHERE completed=?;",(False,))
    return [ x[0] for x in db_cursor.fetchall() ]

def delete_task_from_db ( task_id ):
    db_cursor.execute("DELETE FROM tasks WHERE id=?;",(task_id,))
    db_cursor.execute("DELETE FROM keywords WHERE task_id=?;",(task_id,))

def get_tasks_with_keywords ( keywords ):
    db_cursor.execute("SELECT task_id FROM keywords WHERE keyword IN (%s) GROUP BY task_id;" % ("?,"*len(keywords))[:-1],keywords)
    return [ x[0] for x in db_cursor.fetchall() ]

def close_db ( ):
    db_connection.commit()
    db_connection.close()

#########################
#   Global Variables    #
#########################


kflag = "-k"            # Keywords
pflag = "-p"            # Priority

#########################
#   Parsing Functions   #
#########################

def grab_description ( _args ):
    """Helper function to grab the description of the task"""

    if kflag in _args:
        k_index = _args.index(kflag)
    else:
        k_index = float('inf') # Infinity

    if pflag in _args:
        p_index = _args.index(pflag)
    else:
        p_index = float('inf') # Infinity

    first_flag = min(k_index, p_index)

    try:
        first_flag = int(first_flag)
    except:
        first_flag = None

    return " ".join(_args[:first_flag])

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
            priority = constants.DEFAULT_PRIORITY
    else:
        priority = constants.DEFAULT_PRIORITY
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
        # be a keyword.  You can have multiple-word keywords by surrounding
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

    description = grab_description(_args)
    if not description:
        print 'No description provided!'
    else:
        keywords = grab_keywords(_args)
        priority = grab_priority(_args)

        task_id = add_task_to_db(description,priority)
        for keyword in keywords:
            add_keyword_to_db(task_id,keyword)
        print 'Added:'
        print Task(task_id, description, priority, keywords)

    close_db()
# end def add ( )

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
        task = get_task_by_id(taskid)
        print 'Deleting...\n%s' % task
        delete_task_from_db(taskid)
    except ValueError:
        print "Failed."
        print "'delete' command requires an integer-based task ID."
        print "Please execute 'todo help' for further assistance."

    close_db()
# end def delete ( )

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
        db_cursor.execute("UPDATE tasks SET completed=1 WHERE id=?;",(taskid,))
        print 'Completing...\n%s' % get_task_by_id(taskid)
    except ValueError:
        print "Failed."
        print"'complete' command requires an integer-based task ID."
        print "Please execute 'todo help' for further assistance."

    close_db()
# end def complete ( )

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

    print 'Finished Tasks...'
    id_list = get_list_of_completed_tasks()
    for task_id in id_list:
        print get_task_by_id(task_id)

    close_db()
# end def update ()

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
    print 'looking for %s ...' % _args,
    id_list = get_tasks_with_keywords(_args)
    count = len(id_list)
    print "%s found" % count
    for x in id_list:
        print get_task_by_id(x)

    close_db()
# end def find ( )

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
 _tasks   ID: 1   Done: False   Task: call fred later
            Priority: 10    Keywords: ['foo', 'bar', 'baz']
"""
    print 'Listing most recent tasks...',
    recent = get_list_of_uncompleted_tasks()
    count = len(recent)
    if not count:
        print "None found!"
        print "Unable to find unfinished tasks.  Add a new task to fix this!"
    else:
        print "%s found!" % count
        for x in recent:
            print get_task_by_id(x)

    close_db()
# end def recent ( )

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
