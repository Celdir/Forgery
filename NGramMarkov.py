import sys
from numpy import random

USE_CHARS = True

class Markov:
    def __init__(self, n):
        self.transitions = {}
        self.total = {}
        self.seen = set()
        self.n = n

    """ key is a list of n-1 words and value is a single word """
    def _learn_ngram(self, key, value):
        if key not in self.transitions:
            self.transitions[key] = {}
            self.total[key] = 0
        if value not in self.transitions[key]:
            self.transitions[key][value] = 0
        self.transitions[key][value] += 1
        self.total[key] += 1

    def learn(self, tokens):
        for token in tokens:
            self.seen.add(token)
        for i in range(len(tokens)-self.n):
            self._learn_ngram(tuple(tokens[i:i+self.n-1]), tokens[i+self.n-1])

    def predict(self, key):
        if key not in self.transitions:
            return random.choice(self.seen)
        weights = self.transitions[key].values()
        s = sum(weights)
        return random.choice(self.transitions[key].keys(), p=map(lambda x: float(x)/s, weights))

    def generate(self, base, amount):
        tokens = list(base) if USE_CHARS else base.split()
        self.learn(tokens)
        start = random.randint(0, len(tokens)-self.n)
        gen = tokens[start:start+self.n-1]
        for i in range(amount-(self.n-1)):
            gen.append(self.predict(tuple(gen[-self.n+1:])))
        return ''.join(gen) if USE_CHARS else ' '.join(gen)


def main():
    n = int(sys.argv[2])
    amount = int(sys.argv[3])
    with open(sys.argv[1], 'r') as source:
        m = Markov(n)
        print m.generate(source.read().lower(), amount)

if __name__ == "__main__":
    main()
