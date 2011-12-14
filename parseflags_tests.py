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
from task_commands import grab_priority, grab_keywords, grab_description

class TestArgumentParsing(unittest.TestCase):
    def setUp(self):
        self.empty_str = ''
        # kflag w/ keywords, then pflag w/ priority
        self.args_1 = ['this', 'is', 'a', 'test', '-k','frank', '-p', '500']
        # pflag w/ priority followed by extra text that's ignored
        self.args_2 = ['a really long one', '-p', '100', 'fred', 'ted']
         # pflag followed by kflag w/ no priority declared
        self.args_3 = ['is', 'long combined','-p', '-k', 'foo', 'bar']
        # Everything is ignored
        self.args_4 = ['-pk', 'no', 'way']
        # kflag by itself, will result in empty keywords
        self.args_5 = ['-k']
        # pflag by itself, will result in default priority, 0
        self.args_6 = ['-p']
        # pflag and large priority
        self.args_7 = ['-p', '2352340']
        # kflag with large single keyword
        self.args_8 = ['-k', 'this is 1 keyword']
        # kflag w/out keywords followed by pflag and priority
        self.args_9 = ['-k', '-p', '300']
        # pflag, priority then kflag and keywords]
        self.args_10 = ['-p', '10', '-k', 'foo', 'bar', 'baz']
        self.empty_args = []

    def test_empty_string(self):
        self.assertEqual(grab_keywords(self.empty_str), self.empty_args)

    def test_keywords_flag(self):
        self.assertEqual(grab_keywords(self.args_1),     ['frank'])
        self.assertEqual(grab_keywords(self.args_2),     self.empty_args)
        self.assertEqual(grab_keywords(self.args_3),     ['foo', 'bar'])
        self.assertEqual(grab_keywords(self.args_4),     self.empty_args)
        self.assertEqual(grab_keywords(self.args_5),     self.empty_args)
        self.assertEqual(grab_keywords(self.args_6),     self.empty_args)
        self.assertEqual(grab_keywords(self.args_7),     self.empty_args)
        self.assertEqual(grab_keywords(self.args_8), ['this is 1 keyword'])
        self.assertEqual(grab_keywords(self.args_9),     self.empty_args)
        self.assertEqual(grab_keywords(self.args_10),['foo', 'bar', 'baz'])
        self.assertEqual(grab_keywords(self.empty_args), self.empty_args)

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

    def test_description_parse(self):
        self.assertEqual(grab_description(self.args_1), 'this is a test')
        self.assertEqual(grab_description(self.args_2), 'a really long one')
        self.assertEqual(grab_description(self.args_3), 'is long combined')
        self.assertEqual(grab_description(self.args_4),        '-pk no way')
        self.assertEqual(grab_description(self.args_5),        '')
        self.assertEqual(grab_description(self.args_6),        '')
        self.assertEqual(grab_description(self.args_7),        '')
        self.assertEqual(grab_description(self.args_8),        '')
        self.assertEqual(grab_description(self.args_9),        '')
        self.assertEqual(grab_description(self.args_10),       '')
        self.assertEqual(grab_description(self.empty_args),    '')


suite = unittest.TestLoader().loadTestsFromTestCase(TestArgumentParsing)
unittest.TextTestRunner(verbosity=2).run(suite)
