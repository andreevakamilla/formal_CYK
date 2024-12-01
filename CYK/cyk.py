class CYKAlgorithm:
    def __init__(self, grammar):
        self.grammar = grammar
        self.dp = {}

    def cyk(self, word):
        if word == "e": 
            return 'S' in self.grammar.epsilon_left_part

        n = len(word)
        for non_terminal in self.grammar.rules:
            self.dp[non_terminal] = [[False] * n for _ in range(n)]

        for i, char in enumerate(word):
            for left_part, right_parts in self.grammar.rules.items():
                for right_part in right_parts:
                    if len(right_part) == 1 and right_part[0] == char:
                        self.dp[left_part][i][i] = True

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    for left_part, right_parts in self.grammar.rules.items():
                        for right_part in right_parts:
                            if len(right_part) == 2:
                                B, C = right_part
                                if self.dp[B][i][k] and self.dp[C][k + 1][j]:
                                    self.dp[left_part][i][j] = True

        return self.dp['S'][0][n - 1]
