#################################################
#                                               #
# parseflags_tests.py                           #
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

import unittest
from taskcomm import grab_priority, grab_keywords

class TestGrabKeywords(unittest.TestCase):
    def setUp(self):
        self.empty_str = ''
        self.args_1 = ['-k','frank','hank','tank', '-p', '500'] # kflag w/ keywords, then pflag w/ priority
        self.args_2 = ['-p', '100', 'fred', 'ted']      # pflag w/ priority followed by extra text that's ignored
        self.args_3 = ['-p', '-k', 'foo', 'bar']        # pflag followed by kflag w/ no priority declared
        self.args_4 = ['-pk', 'no', 'way'] # Everything is ignored
        self.args_5 = ['-k'] # kflag by itself, will result in empty keywords
        self.args_6 = ['-p'] # pflag by itself, will result in default priority, 0
        self.args_7 = ['-p', '2352340'] # pflag and large priority
        self.args_8 = ['-k', 'this is a long keyword'] # kflag with large single keyword
        self.args_9 = ['-k', '-p', '300'] # kflag w/out keywords followed by pflag and priority
        self.args_10 = ['-p', '10', '-k', 'foo', 'bar', 'baz'] # pflag, priority then kflag and keywords
        self.empty_args = []

    def test_empty_string(self):
        self.assertEqual(grab_keywords(self.empty_str), self.empty_args)

    def test_keywords_flag(self):
        self.assertEqual(grab_keywords(self.args_1),        ['frank','hank','tank'])
        self.assertEqual(grab_keywords(self.args_2),        self.empty_args)
        self.assertEqual(grab_keywords(self.args_3),        ['foo', 'bar'])
        self.assertEqual(grab_keywords(self.args_4),        self.empty_args)
        self.assertEqual(grab_keywords(self.args_5),        self.empty_args)
        self.assertEqual(grab_keywords(self.args_6),        self.empty_args)
        self.assertEqual(grab_keywords(self.args_7),        self.empty_args)
        self.assertEqual(grab_keywords(self.args_8),        ['this is a long keyword'])
        self.assertEqual(grab_keywords(self.args_9),        self.empty_args)
        self.assertEqual(grab_keywords(self.args_10),       ['foo', 'bar', 'baz'])
        self.assertEqual(grab_keywords(self.empty_args),    self.empty_args)

    def test_priority_flag(self):
        self.assertEqual(grab_priority(self.args_1),        500)
        self.assertEqual(grab_priority(self.args_2),        100)
        self.assertEqual(grab_priority(self.args_3),        0)
        self.assertEqual(grab_priority(self.args_4),        0)
        self.assertEqual(grab_priority(self.args_5),        0)
        self.assertEqual(grab_priority(self.args_6),        0)
        self.assertEqual(grab_priority(self.args_7),        2352340)
        self.assertEqual(grab_priority(self.args_8),        0)
        self.assertEqual(grab_priority(self.args_9),        300)
        self.assertEqual(grab_priority(self.args_10),       10)
        self.assertEqual(grab_priority(self.empty_args),    0)

suite = unittest.TestLoader().loadTestsFromTestCase(TestGrabKeywords)
unittest.TextTestRunner(verbosity=2).run(suite)
