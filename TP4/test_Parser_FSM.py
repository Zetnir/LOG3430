import unittest
import unittest.mock
import os
from Parser_FSM import ApplyRules, RuleGroup, Rule, S_NEW_GROUP, S_PRE
from unittest.mock import MagicMock, Mock

class TestParserFSM(unittest.TestCase):
    def setUp(self):
        pass

    def test_the_first_state_for_all_cases_should_be_new_group_state(self):
        test_string = ""
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_NEW_GROUP)

    def test_when_value_is_a_letter_state_should_be_pre(self):
        test_string = "p"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_PRE)
    
    def test_when_value_starts_with_a_letter_and_is_followed_by_letters_state_should_stay_in_pre(self):
        test_string = "print"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_PRE)