# Probing of pretrained multilingual models on the knowledge of discourse on the material of Universal Dependencies
In our study we tried to accumulate all kinds of tasks used for discourse probing making them multilingual and testing four models:
- BERT multilingual base model (cased) 
- XLM-RoBERTa (base-sized model) 
- Multilingual GPT model 
- mT5 model 
The tasks we have compiled for different models have already been used in other probing studies. At the same time, we tried to make a collection of tasks from different previous works in order to compare the results obtained and identify new problems in the assimilation of the text discourse by neural networks. We are also interested in how differently the models perform depending on the language in which the text is written.
We frame almost all presented tasks as binary classification problems, but they involve different aspects of Rhetorical Structure Theory, models’ understanding of which is being tested in this study. The peculiarity of our work is that we test multilingual, rather than basic, models on the corresponding data for ten languages, exploring only modern pre-trained transformer models.
#### Sentence Position 
We decided to take 5-sentence sequences for our dataset and swap the fourth of them with the other randomly chosen sentence in a sequence. This method was partly proposed by our predecessors, and, although in the described article researchers swap the forth sentence with the first one, we decided not to swap fixed elements of a text, and choose one of them randomly, so we complicated the task, because usually models demonstrate high results in this test. 
#### Binary sentence ordering 
Binary Sentence Ordering (BSO) is a binary classification task to determine the order of two sentences. This task differs from SP in that a much smaller amount of context is supplied to the input, so this test allows us to evaluate the ability of the model to determine the relationship between the minimum context of two sentences.
#### Discourse Coherence 
The task is to determine whether a sequence of six sentences forms a coherent paragraph. Connectivity within the document, in accordance with our research and the previous work, is determined from 6 sentences. In our case, this number is fixed. Negative examples are created by replacing one of the sentences with a sentence from another text.
#### Next sentence prediction 
In the source paper there were 3 negative candidates and a single positive one for the next sentence, but we adopted it as a binary classification problem, therefore, for negative examples of sequences we shuffle the last sentence with the other sentence, but not within one document to sustain the text structure. 
#### Sentence ordering 
Originally this task was done by shuffling from 3 to 7 sentences, providing the model with the correct ordering and then predicting it. We reworked it by shuffling all the sentences for the incorrect sequences.
#### Discourse connective prediction 
We predict connectives which occur in the beginning of the sentence, considering this as a base position for an explicit binding marker. This choice is explained by the fact that before testing the understanding of implicit connectives by a multilingual model, we must first pay attention to explicit ones
#### Cloze story test 
In this task the model receives a document containing 4 sentences as input and chooses the best completion for the text. We changed this task by making the answers binary and shuffling the last sentences in the sequence for negative samples.
