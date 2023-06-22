import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

df = pd.read_csv('Keywords_domains.csv')
df2 = pd.read_csv('Technology_name.csv')

df = df.astype(str)
df2 = df2.astype(str)

keywords = df['Technology'].tolist()
video_names = df2['Title'].tolist()

training_data = [str(keyword) + " " + str(video_name) for keyword, video_name in zip(keywords, video_names)]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(training_data)
total_words = len(tokenizer.word_index) + 1

input_sequences = []
for line in training_data:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

max_sequence_length = max([len(seq) for seq in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre'))

X_train = input_sequences[:, :-1]
y_train = input_sequences[:, -1]
y_train = to_categorical(y_train, num_classes=total_words)

model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_length-1))
model.add(LSTM(150))
model.add(Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=50, verbose=1)

# def generate_video_name(seed_text, next_words, model, max_sequence_length):
#     for _ in range(next_words):
#         token_list = tokenizer.texts_to_sequences([seed_text])[0]
#         token_list = pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
#         predicted = np.argmax(model.predict(token_list), axis=-1)
#         output_word = ""
#         for word, index in tokenizer.word_index.items():
#             if index == predicted:
#                 output_word = word
#                 break
#         seed_text += " " + output_word
#     return seed_text

# seed_text = "Technology"
# num_suggestions = 5
# generated_names = generate_video_name(seed_text, num_suggestions, model, max_sequence_length)

# for i, name in enumerate(generated_names, start=1):
#     print(f"Suggestion {i}: {name}")
# Generate new video name suggestions
def generate_video_name(seed_text, next_words, model, max_sequence_length):
    generated_names = []
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
        generated_names.append(output_word)
    return ' '.join(generated_names)

# Set the seed text and generate video name suggestions
seed_text = "Technology"
num_suggestions = 5
generated_names = generate_video_name(seed_text, num_suggestions, model, max_sequence_length)

# Print the generated video name suggestions
print(f"Suggested video names: {generated_names}")
