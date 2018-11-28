import sys
import numpy as np
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.models import Sequential
from keras.utils import np_utils

np.random.seed(823)

USE_CHARS = True

class NeuralNet:
    def __init__(self, n):
        self.n = n
        self.token_to_index = {}
        self.index_to_token = {}
        self.sequence = []
        self.result = []
        self.seq_transform = []
        self.res_transform = []
        self.seen = set()
        self.model = None

    def learn(self, tokens):
        self.seen = sorted(set(tokens))
        self.token_to_index = {t : i for i, t in enumerate(self.seen)}
        self.index_to_token = {i : t for i, t in enumerate(self.seen)}

        for i in range(len(tokens)-self.n):
            prefix = tokens[i:i+self.n]
            suffix = tokens[i+self.n]
            self.sequence.append([self.token_to_index[token] for token in prefix])
            self.result.append(self.token_to_index[suffix])
        self.seq_transform = np.reshape(self.sequence, (len(self.sequence), self.n, 1)) / float(len(self.seen))
        self.res_transform = np_utils.to_categorical(self.result)

        self.model = Sequential()
        self.model.add(LSTM(500, input_shape=self.seq_transform.shape[1:3], return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(500, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(500))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(self.res_transform.shape[1], activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')
        #self.model.fit(self.seq_transform, self.res_transform, epochs=100, batch_size=50)
        #self.model.save_weights('training_weights')
        self.model.load_weights('training_weights')

    def predict(self, key):
        if key not in self.transitions:
            return np.random.choice(self.seen)
        weights = self.transitions[key].values()
        s = sum(weights)
        return np.random.choice(self.transitions[key].keys(), p=map(lambda x: float(x)/s, weights))

    def generate(self, base, amount):
        tokens = list(base) if USE_CHARS else base.split()
        self.learn(tokens)

        prefix = self.sequence[np.random.randint(len(self.sequence))]
        gen = [self.index_to_token[t] for t in prefix]
        for i in range(amount):
            cur = np.reshape(prefix, (1, len(prefix), 1))
            cur = cur / float(len(self.seen))

            next_idx = np.argmax(self.model.predict(cur, verbose=0))
            gen.append(self.index_to_token[next_idx])
            prefix.append(next_idx)
            prefix = prefix[1:]
        return ''.join(gen) if USE_CHARS else ' '.join(gen)


def main():
    n = int(sys.argv[2])
    amount = int(sys.argv[3])
    with open(sys.argv[1], 'r') as source:
        m = NeuralNet(n)
        text = ' '.join(source.read().split())
        print m.generate(text, amount)

if __name__ == "__main__":
    main()
