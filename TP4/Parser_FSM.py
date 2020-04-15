import re


def tr_newG(obj_state):
    obj_state.group_current_level += 1
    obj_state.current_group = RuleGroup(obj_state.current_group, obj_state.group_current_level, None)


def tr_Append_Preconditon(obj_state):
    rule_count = obj_state.current_group.rule_count
    obj_state.current_group.rules[rule_count - 1].prefix += obj_state.current_char


def tr_add_operator(obj_state):
    rule_count = obj_state.current_group.rule_count
    obj_state.current_group.rules[rule_count - 1].op = obj_state.current_char


def tr_end_group(obj_state):
    obj_state.group_current_level += 1
    obj_state.current_group = RuleGroup(obj_state.current_group, obj_state.group_current_level, None)


def tr_end_rule(obj_state):
    pass


def tr_add_operator_new_rule(obj_state):
    obj_state.current_group.rule_count += 1
    obj_state.current_group.rules.append(Rule())
    rule_count = obj_state.current_group.rule_count
    obj_state.current_group.rules[rule_count - 1].op = obj_state.current_char


def tr_add_subj(obj_state):
    rule_count = obj_state.current_group.rule_count
    obj_state.current_group.rules[rule_count - 1].subject += obj_state.current_char

def tr_pass(obj_state):
    # Do nothing just pass to the next char
    pass

def tr_add_operator_new_group(obj_state):
    obj_state.current_group.op = obj_state.current_char


T_SKIP = tr_pass  # pass
T_NEW_GROUP = tr_newG  # new group
T_APPEND_CHAR_PRE = tr_Append_Preconditon  # add a precondition
T_ADD_OP = tr_add_operator  # add an operator
T_ADD_OP_NEW_RULE = tr_add_operator_new_rule
T_END_GROUP = tr_end_group
T_END_RULE = tr_end_rule
T_APPEND_CHAR_SUBJ = tr_add_subj
T_ADD_GROUP_OP = tr_add_operator_new_group

S_NEW_GROUP = "STATE: NEW_GROUP"
S_END_GROUP = "STATE: END_GROUP"
S_PRE = "STATE: PREFIX"
S_OP = "STATE: OPERATOR"
S_END_RULE = "STATE: END_RULE"
S_SUBJ = "STATE: SUBJECT"

FSM_MAP = (
    #  {'src':, 'dst':, 'condition':, 'callback': },
    {'src': S_NEW_GROUP,
     'dst': S_PRE,
     'condition': "[A-Za-z|+|-|\d]",
     'callback': T_APPEND_CHAR_PRE},
    {'src': S_PRE,
     'dst': S_PRE,
     'condition': "[A-Za-z|+|-|\d]",
     'callback': T_APPEND_CHAR_PRE},
    {'src': S_PRE,
     'dst': S_SUBJ,
     'condition': "\(",
     'callback': T_SKIP},  # 3
    {'src': S_SUBJ,
     'dst': S_SUBJ,
     'condition': "[^\)]",
     'callback': T_APPEND_CHAR_SUBJ},
    {'src': S_SUBJ,
     'dst': S_END_RULE,
     'condition': "\)",
     'callback': T_END_RULE},
    {'src': S_END_RULE,
     'dst': S_END_GROUP,
     'condition': "\)",
     'callback': T_END_GROUP},
    {'src': S_END_RULE,
     'dst': S_OP,
     'condition': "[\&|\|]",
     'callback': T_ADD_OP_NEW_RULE},
    {'src': S_END_GROUP,
     'dst': S_OP,
     'condition': "[\&|\|]",
     'callback': T_ADD_GROUP_OP},
    {'src': S_OP,
     'dst': S_NEW_GROUP,
     'condition': "\(",
     'callback': T_NEW_GROUP},
    {'src': S_OP,
     'dst': S_PRE,
     'condition': "[A-Za-z|+|-|\d]",
     'callback': T_APPEND_CHAR_PRE},
    {'src': S_SUBJ,
     'dst': S_END_RULE,
     'condition': "\)",
     'callback': T_END_RULE})

for map_item in FSM_MAP:
    map_item['condition_re_compiled'] = re.compile(map_item['condition'])


class Rule:
    def __init__(self):
        self.prefix = ""
        self.subject = ""
        self.op = None

    def __repr__(self):
        op = self.op
        if not op:
            op = ''
        return "<Rule: {} {}({})>".format(op, self.prefix, self.subject)


class RuleGroup:
    def __init__(self, parent, level, op):
        self.op = op
        self.parent = parent
        self.level = level
        self.rule_count = 1
        self.rules = [Rule(), ]

    def __repr__(self):
        return "<RuleGroup: {}>".format(self.__dict__)


class ApplyRules:

    def __init__(self, input_str):
        self.input_str = input_str
        self.current_state = S_NEW_GROUP
        self.group_current_level = 0
        self.current_group = RuleGroup(None, self.group_current_level, None)
        self.current_char = ''

    def run(self):
        for c in self.input_str:
            if not self.go_next(c):
                print("skip '{}' in {}".format(c, self.current_state))


    def go_next(self, achar):
        self.current_char = achar
        frozen_state = self.current_state
        for transition in FSM_MAP:
            if transition['src'] == frozen_state:
                if self.iterate_re_evaluators(achar, transition):
                    return True
        return False

    def iterate_re_evaluators(self, achar, transition):
        condition = transition['condition_re_compiled']
        if condition.match(achar):
            self.update_state(
                transition['dst'], transition['callback'])
            return True
        return False

    def update_state(self, new_state, callback):
        print("{} -> {} : {}".format(self.current_char,
                                     self.current_state,
                                     new_state))
        self.current_state = new_state
        callback(self)


# -------------------------------
#str = "print(bonjour (log3430())) !"
str = "print(bonjour log3430)"
# str = "a = 3 +4 * 5 & print(a)"
print("instruction: " + str)
print("----------------------")
parse = ApplyRules(str)
parse.run()
print("----------------------")
print(parse.current_group)
