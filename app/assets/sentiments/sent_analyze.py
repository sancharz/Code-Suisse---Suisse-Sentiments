from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.sentiment.util import *

#article is a string representing the contents of the article
def analyzer (article):
	#document represented by a tuple (sentence,labelt)
	n_instances = 100
	subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
	obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]

	#split subj and objinstances to keep a balanced uniform class distribution in both train and test sets.
	train_subj_docs = subj_docs[:80]
	test_subj_docs = subj_docs[80:100]
	train_obj_docs = obj_docs[:80]
	test_obj_docs = obj_docs[80:100]
	training_docs = train_subj_docs+train_obj_docs
	testing_docs = test_subj_docs+test_obj_docs

	sentim_analyzer = SentimentAnalyzer()
	all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

	#use simple unigram word features, handling negation
	unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
	sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

	#apply features to obtain a feature_value representations of our datasets
	training_set = sentim_analyzer.apply_features(training_docs)
	test_set = sentim_analyzer.apply_features(testing_docs)

	#train classifier 
	trainer = NaiveBayesClassifier.train
	classifier = sentim_analyzer.train(trainer, training_set)
	for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
		print('{0}: {1}'.format(key, value))

	sid = SentimentIntensityAnalyzer()
	return sid.polarity_scores(article)

