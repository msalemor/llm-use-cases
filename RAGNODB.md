## RAG no VectorDB


```python
prompt_template = """Using only the best answers, answer the following question: "
{{$input}}


Text: ###
1. CRISPR (Clustered Regularly Interspaced Short Palindromic Repeats) is a revolutionary gene-editing tool that allows precise modification of an organism's DNA. It can be used to correct genetic defects, create genetically modified organisms, study gene functions, and potentially treat various diseases by editing the DNA sequence.

2. Blockchain is a decentralized, distributed ledger technology. It ensures security through cryptographic techniques and consensus protocols. Each block in the chain contains a cryptographic hash of the previous block, making it tamper-evident. Transactions are validated by multiple participants (nodes) in the network, enhancing security and preventing unauthorized changes.

3. Quantum computing leverages the principles of quantum mechanics to perform computations using quantum bits (qubits), which can exist in multiple states simultaneously, unlike classical bits that are either 0 or 1. This ability for qubits to exist in superposition allows quantum computers to solve certain complex problems much faster than classical computers.

4. Machine learning is a subset of artificial intelligence where systems learn from data and improve their performance over time without being explicitly programmed. Its applications range from recommendation systems in online platforms, fraud detection in financial transactions, autonomous vehicles, natural language processing, to medical diagnostics and image recognition.

5. Self-driving cars use a combination of sensors such as cameras, lidar, radar, and GPS to perceive the environment. These sensors collect data, which is processed by sophisticated algorithms to create a real-time map of the car's surroundings. Decision-making algorithms then analyze this data to make decisions about steering, acceleration, and braking, allowing the vehicle to navigate and operate autonomously.

6. NFTs are a specialized application of blockchain technology, utilizing its security and decentralization to authenticate and establish ownership of digital assets that are unique and non-interchangeable.

###

Output format: ###
Question: ''
Answer: ''
###


Use only the provided text. Provide the original question and the answer. If the question cannot be answered from the text, answer "I don't know. 

"""
max_tokens = common.get_max_tokens(prompt_template)+100
search_func = kernel.create_semantic_function(prompt_template, temperature=0.3, max_tokens=max_tokens)


print(search_func("What is a CRISPR?"))
print(search_func("What is an NFT?"))
print(search_func("What is the speed of light?"))
```

Output:

```text

```
