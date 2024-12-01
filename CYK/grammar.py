from collections import defaultdict, deque


class Grammar:
    def __init__(self):
        self.rules = defaultdict(list)  
        self.epsilon_left_part = set() 
        self.used_symbols = [-1] * 26  
        self.first_available_symbol = 0
        self.used_terminals = ['1'] * 26  

    def is_terminal(self, symbol):
        return symbol.islower()

    def insert_rule(self, left_part, right_part):
        self.rules[left_part].append(right_part)

    def add_rule(self, rule):
        left_part = rule[0]
        right_part = rule[3:] if len(rule) > 3 else ""
        self.used_symbols[ord(left_part) - ord('A')] = -1
        if right_part == "e":
            self.epsilon_left_part.add(left_part)
            return
        self.insert_rule(left_part, right_part)

    def delete_long_rules(self):
        queue = deque()
        for left_part, right_parts in self.rules.items():
            for i, right_part in enumerate(right_parts):
                if len(right_part) > 2:
                    while self.used_symbols[self.first_available_symbol] != -1:
                        self.first_available_symbol += 1
                    new_left_part = chr(self.first_available_symbol + ord('A'))
                    tmp = right_part[1:]
                    queue.append((new_left_part, tmp))
                    new_rule = right_part[0] + new_left_part
                    self.used_symbols[self.first_available_symbol] = True
                    self.rules[left_part][i] = new_rule

        while queue:
            left_part, right_part = queue.popleft()
            if len(right_part) > 2:
                while self.used_symbols[self.first_available_symbol] != -1:
                    self.first_available_symbol += 1
                new_left_part = chr(self.first_available_symbol + ord('A'))
                tmp = right_part[1:]
                queue.append((new_left_part, tmp))
                self.rules[left_part].append(right_part[0] + new_left_part)
            else:
                self.rules[left_part].append(right_part)

    def find_epsilon(self):
        is_change = True
        while is_change:
            is_change = False
            for left_part, right_parts in self.rules.items():
                if left_part in self.epsilon_left_part:
                    continue
                for right_part in right_parts:
                    if all(symbol in self.epsilon_left_part for symbol in right_part):
                        self.epsilon_left_part.add(left_part)
                        is_change = True
                        break

    def delete_epsilon(self):
        self.find_epsilon()
        new_rules = defaultdict(list)
        for left_part, right_parts in list(self.rules.items()):  
            for right_part in right_parts:
                if len(right_part) == 1 and right_part[0] in self.epsilon_left_part:
                    for sub_rule in self.rules[right_part[0]]:
                        new_rules[left_part].append(sub_rule)
                else:
                    new_rules[left_part].append(right_part)
        self.rules = new_rules

    def delete_chain_rules(self):
        keys = list(self.rules.keys())  
        for left_part in keys:
            self._check_chain_rules(left_part)

    def _check_chain_rules(self, symbol):
        new_rules = []
        original_rules = list(self.rules[symbol]) 
        for right_part in original_rules:
            if len(right_part) == 1 and not self.is_terminal(right_part[0]) and right_part[0].isalpha():
                self._check_chain_rules(right_part[0])
                new_rules.extend(self.rules[right_part[0]])
            else:
                new_rules.append(right_part)
        self.rules[symbol] = new_rules

    def delete_multiple_terminals(self):
        new_rules = defaultdict(list) 
        for left_part, right_parts in list(self.rules.items()): 
            for right_part in right_parts:
                if len(right_part) == 2:
                    updated_right_part = list(right_part)  
                    for i, symbol in enumerate(right_part):
                        if self.is_terminal(symbol) or not symbol.isalpha():  
                            if self.used_terminals[ord(symbol) - ord('a')] == '1': 
                                while self.used_symbols[self.first_available_symbol] != -1:
                                    self.first_available_symbol += 1
                                new_symbol = chr(self.first_available_symbol + ord('A'))
                                self.used_symbols[self.first_available_symbol] = True
                                self.used_terminals[ord(symbol) - ord('a')] = new_symbol
                                new_rules[new_symbol].append(symbol) 
                                updated_right_part[i] = new_symbol
                            else: 
                                updated_right_part[i] = self.used_terminals[ord(symbol) - ord('a')]
                    new_rules[left_part].append("".join(updated_right_part)) 
                else:
                    new_rules[left_part].append(right_part) 
        self.rules.update(new_rules)  

    def grammar_to_chomsky(self):
        self.delete_long_rules()
        self.delete_epsilon()
        self.delete_chain_rules()
        self.delete_multiple_terminals()
