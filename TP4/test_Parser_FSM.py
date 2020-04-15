import unittest
import unittest.mock
import os
from Parser_FSM import ApplyRules, RuleGroup, Rule, S_NEW_GROUP, S_PRE, S_SUBJ, S_END_RULE, S_END_GROUP, S_OP
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

    def test_when_first_char_is_a_letter_state_should_move_to_pre(self):
        test_string = "p"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_PRE)

    def test_when_char_does_not_start_with_a_letter_state_should_be_new_group(self):
        test_string = "("
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_NEW_GROUP)
    
    def test_when_value_started_with_a_letter_and_is_followed_by_letters_state_should_stay_in_pre(self):
        test_string = "pr"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_PRE)

    def test_when_adding_a_left_bracket_to_a_value_a_pre_state_shoud_change_to_subject_state(self):
        test_string = "print("
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_SUBJ)

    def test_when_adding_characters_beside_right_bracket_to_value_in_subject_state_should_stay_in_subject_state(self):
        test_string = "print(test"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_SUBJ)

    def test_when_adding_right_bracket_to_value_in_subject_state_should_change_to_end_rule(self):
        test_string = "print(test)"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_END_RULE)

    def test_when_adding_right_bracket_to_value_in_end_rule_state_should_change_to_end_group(self):
        test_string = "print(test))"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_END_GROUP)

    def test_when_adding_and_operators_to_value_in_end_group_state_should_change_to_op(self):
        test_string = "print(test))&"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_OP)

    def test_when_adding_or_operators_to_value_in_end_group_state_should_change_to_op(self):
        test_string = "print(test))|"
        parse = ApplyRules(test_string)
        parse.run()
        print(parse.current_state)
        self.assertEqual(parse.current_state, S_OP)