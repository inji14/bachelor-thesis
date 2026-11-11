
import numpy as np

# generate some random plaintext and key
plaintext = input("Enter a plaintext: ") #'I have it all done'
key = input("Enter a key: ")#'secret'

# encrypt the plaintext using the Vigenère cipher
def vigenere_encipher(plaintext, key):
    ciphertext = ''
    for i in range(len(plaintext)):
        pi = ord(plaintext[i]) - 97
        ki = ord(key[i % len(key)]) - 97
        ci = (pi + ki) % 26
        ciphertext += chr(ci + 97)
    return ciphertext

ciphertext = vigenere_encipher(plaintext, key)

# generate the feature vectors
def gen_feature_vectors(ciphertext, m):
    feature_vectors = []
    for i in range(len(ciphertext) - m):
        feature_vector = [0] * 26
        for j in range(m):
            index = ord(ciphertext[i + j]) - 97
            feature_vector[index] += 1
        feature_vectors.append(feature_vector)
    return feature_vectors

# generate the labels
def gen_labels(ciphertext, m):
    labels = []
    for i in range(len(ciphertext) - m):
        labels.append(ord(ciphertext[i + m]) - 97)
    return labels

# generate the training and testing data
m = 6
feature_vectors = np.array(gen_feature_vectors(ciphertext, m))
labels = np.array(gen_labels(ciphertext, m))

split = int(0.8 * len(feature_vectors))
train_X = feature_vectors[:split]
train_y = labels[:split]
test_X = feature_vectors[split:]
test_y = labels[split:]

# train the model
from sklearn.neural_network import MLPClassifier

model = MLPClassifier(hidden_layer_sizes=(100, 100))
model.fit(train_X, train_y)

# predict the next character
def predict_next_character(ciphertext, key, m, model):
    feature_vector = gen_feature_vectors(ciphertext, m)[-1]
    label = model.predict([feature_vector])[0]
    next_char = chr((label + 97) % 26 + 97)
    key += next_char
    ciphertext += next_char
    return ciphertext, key

# decrypt the ciphertext
key = ''
while len(key) < len(plaintext):
    ciphertext, key = predict_next_character(ciphertext, key, m, model)

print(f'ciphertext: {ciphertext}')
print(f'key: {key}')
