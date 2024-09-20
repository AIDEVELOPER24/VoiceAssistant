import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout, SpatialDropout1D
from sklearn.model_selection import train_test_split
import pickle

# Load the JSON dataset
intents_path = 'intents.json'
with open(intents_path) as file:
    data = json.load(file)

# Prepare the data
training_sentences = []
training_labels = []
labels = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

# Convert labels to numerical data
num_classes = len(labels)
label_tokenizer = LabelEncoder()
label_tokenizer.fit(labels)
training_labels = label_tokenizer.transform(training_labels)

# Tokenize the training sentences
vocab_size = 5000
embedding_dim = 100
max_len = 30
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(padded_sequences, training_labels, test_size=0.2, random_state=42)

# Build the model
model = Sequential([
    Embedding(vocab_size, embedding_dim, input_length=max_len),
    SpatialDropout1D(0.2),
    LSTM(128, return_sequences=True),
    LSTM(64),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
epochs = 100
batch_size = 32
history = model.fit(X_train, np.array(y_train), epochs=epochs, batch_size=batch_size, validation_data=(X_val, np.array(y_val)), verbose=1)

# Print training results
print("Training completed.")
print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
print(f"Final training loss: {history.history['loss'][-1]:.4f}")
print(f"Final validation loss: {history.history['val_loss'][-1]:.4f}")

# Save the trained model
model_path = 'my_model.keras'
model.save(model_path)

# Save the tokenizer
tokenizer_path = 'tokenizer.pickle'
with open(tokenizer_path, 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save the label encoder
label_encoder_path = 'label_encoder.pickle'
with open(label_encoder_path, 'wb') as ecn_file:
    pickle.dump(label_tokenizer, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)