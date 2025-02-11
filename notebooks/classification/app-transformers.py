from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# Load pre-trained model tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# functions
def get_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt",
                       padding=True, truncation=True)
    outputs = model(**inputs)
    # Using mean of last layer hidden states as the sentence embedding
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()


def calculate_centroid(embeddings):
    return np.mean(embeddings, axis=0)

concrete_sentences = [
    "The cat sat on the mat.",
    "The dog barked loudly.",
    "She baked a cake.",
    "John speaks well"]

abstract_sentences = [
    "Freedom is the right to choose.",
    "Love is eternal.",
    "Happiness is a state of mind.",
    "Freedom of speech is required"]

# Getting embeddings
concrete_embeddings = [get_embedding(sentence)
                       for sentence in concrete_sentences]
abstract_embeddings = [get_embedding(sentence)
                       for sentence in abstract_sentences]

# Calculating average locations (centroids)
concrete_centroid = calculate_centroid(concrete_embeddings)
abstract_centroid = calculate_centroid(abstract_embeddings)

# Classifying a new sentence
new_sentence = "John works every day. "
new_embedding = get_embedding(new_sentence)

# Measuring distances to the centroids
distance_to_concrete = np.linalg.norm(new_embedding-concrete_centroid)
distance_to_abstract = np.linalg.norm(new_embedding-abstract_centroid)

print(distance_to_concrete)
print(distance_to_abstract)

# Classification based on proximity
if distance_to_concrete < distance_to_abstract:
    classification = "Concrete"
else:
    classification = "Abstract"
# print classification
print(classification)


# Concatenate all embeddings
all_embeddings = np.concatenate(
    (concrete_embeddings, abstract_embeddings), axis=0)
all_embeddings = np.squeeze(all_embeddings, axis=1)
print(all_embeddings.shape)

perplexity_value = min(30, len(all_embeddings)-1)
tsn = TSNE(n_components=2, random_state=42, perplexity=perplexity_value)
embeddings_2d = tsn.fit_transform(all_embeddings)

num_concrete = len(concrete_embeddings)

plt.figure(figsize=(10, 6))
plt.scatter(embeddings_2d[:num_concrete, 0],
            embeddings_2d[:num_concrete, 1], color='b', label='Concrete')
plt.scatter(embeddings_2d[num_concrete:, 0],
            embeddings_2d[num_concrete:, 1], color='r', label='Abstract')
plt.title('2D t-SNE of Sentence Embeddings')
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.legend()
plt.grid(True)
plt.show()
