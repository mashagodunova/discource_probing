# discource_probing
#### Sentence Position - sent_posit.py
When constructing this dataset, we take five consecutive sentences from a corpus, randomly move one of these five sentences to the first position, and ask models to predict the true position of the first sentence in the modified sequence.
#### Binary sentence ordering - bin_so.py
Binary Sentence Ordering (BSO) is a binary classification task to determine the order of two sentences.
#### Discourse Coherence (forming paragraph with 6 sentences) - disco_coh.py
The task is to determine whether a sequence of six sentences forms a coherent paragraph. We start with a coherent sequence of six sentences, then randomly replaceone of  the sentences (chosen uniformly among positions 2-5) with a sentence from another discourse.
#### Neighboring Sentence Prediction - nb_pred.py 
In particular, we predict the immediately preceding and succeeding sentences.
#### Nesting level of the sentence - nest.py 
The “nesting level” of a sentence (i.e., how many levels deep it resides) provides information about its role in the overall discourse.
#### Next sentence prediction - next_pred.py
We frame it as a 4-way classification task, with one positive and 3 negative candidates for the next sentence. The preceding context takes the form of between 2 and 8 sentences, but the candidates are always single sentences.
#### Sentence ordering - so_shuf.py
We shuffle 3–7 sentences and attempt to reproduce the original order. This task is assessed based on rank correlation relative to the original order.
#### Discourse connective prediction - conj.py
Given two sentences/clauses, the task is to identify an appropriate discourse marker, such as while, or or although, representing the conceptual relation between the sentences/clauses.
#### Cloze story test - cloze_test.py
Given a 4-sentence story context, pick the best ending from two possible options. This task is harder than NSP, as it requires an understanding of commonsense and storytelling
#### Sentence and paragraph position - sent_par.py
Similar to nesting level, we add a loss based on using the sentence representation to predict its position in the paragraph and in the article.
#### папка outputs:
##### ru-output.tsv 
пример полученного файла для русского языка в результате предобработки для задания "Predicting annotated discourse relations among sentences"
##### ru-sent_ordering.tsv
пример полученного файла для русского языка в результате предобработки для заданий типа "Порядок предложений"
