import spacy
import string
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from gensim.matutils import Sparse2Corpus
from gensim.models.ldamodel import LdaModel
import pyLDAvis
import pyLDAvis.gensim_models
from gensim.corpora.dictionary import Dictionary

df_filtered = pd.read_csv("data/clean_data/full_data_filtered.csv", sep='\t', encoding='utf-8', index_col=False)
nlp = spacy.load('en_core_web_sm')


def split_into_tokens_spacy(desc):
    """
    remove stop words + punctuation and tokenise the sentence
    """
    doc = nlp(desc)
    return [w.text.lower() for w in doc if not (w.is_stop or w.text in string.punctuation)]


tokens_spacy = df_filtered.head(n=1).TXT.apply(split_into_tokens_spacy)[0]
print(tokens_spacy)

bow_transformer = CountVectorizer(tokenizer=split_into_tokens_spacy, min_df=0.01)
# Fit --> "apprentissage" du vocabulaire
bow_transformer.fit(df_filtered.TXT)
# Vocabulaire final : dimension des vecteurs
print(len(bow_transformer.vocabulary_))

# Vocabulaire
feat_names = bow_transformer.get_feature_names()
print(feat_names)

# Transformation de toutes les descriptions en sac de mots
descriptions_bow = bow_transformer.transform(df_filtered.TXT)

frequencies = Counter()
for i, tok in enumerate(feat_names):
    frequencies[tok] = descriptions_bow.getcol(i).sum()
print(frequencies.most_common(10))

wordcloud = WordCloud(background_color="white", max_words=100)
wordcloud.generate_from_frequencies(frequencies)
wordcloud.to_image()
wordcloud.to_file("img/worldcloud.png")

# Transformation du sac de mots au format attendu par Gensim
corpus_bow = Sparse2Corpus(descriptions_bow, documents_columns=False)
# Dictionnaire associant les identifiants des mots du vocabulaire au mot correspondant
id_2_word_dict = {i: feat_names[i] for i in range(len(feat_names))}
# Estimation du modèle LDA à partir du corpus
# Pour une explication des paramètres, voir https://radimrehurek.com/gensim/models/ldamodel.html
lda_model = LdaModel(corpus=corpus_bow,
                     id2word=id_2_word_dict,
                     num_topics=5, chunksize=250,
                     passes=10, per_word_topics=True,
                     random_state=40)
# Récupération des topics
all_topics = lda_model.print_topics(num_words=20)

for idx, topic in all_topics:
    print(f"Topic: {idx} \nWords: {topic}\n")

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus_bow,
                                     Dictionary.from_corpus(corpus_bow, id_2_word_dict),
                                     sort_topics=False)
# Sauvegarde de la visualisation dans un fichier
pyLDAvis.save_html(vis, 'climate_action_lda.html')
