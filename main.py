import sys
from CYK.grammar import Grammar
from CYK.cyk import CYKAlgorithm


def main():
    quantity_rules = int(input(""))
    quantity_words = int(input(""))
    
    grammar = Grammar()
    
    for _ in range(quantity_rules):
        rule = input().strip()
        grammar.add_rule(rule)
    
    grammar.grammar_to_chomsky()
    
    cyk_parser = CYKAlgorithm(grammar)
    
    for _ in range(quantity_words):
        word = input().strip()
        if cyk_parser.cyk(word):
            print("YES")
        else:
            print("NO")



main()
