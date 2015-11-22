import re, string


def tokenize(raw_text, stopwords):
	punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))

	formatted_text = punct.split(query.lower())
	formatted_text = [w for w in formatted_text if (w not in stopwords and not '\[.*\]')]