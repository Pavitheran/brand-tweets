import time

RESULT_DIR = "results"

class TweetAnalyzer(object):
	def __init__(self):
		self.start_time = time.time()
		self.positive_tweets = 0
		self.negative_tweets = 0
		self.neutral_tweets = 0
		self.positive_set = setup_word_set('identifiers/positive-words.txt')
		self.negative_set = setup_word_set('identifiers/negative-words.txt')
		self.pfile = self.create_file("positive_tweets.txt")
		self.nfile = self.create_file("negative_tweets.txt")

	def create_file(self, fname):
		# Creates file under result_root subdirectory.
		path = "{0}/{1}".format(RESULT_DIR, fname)
		# Creates path if it does not exist else truncates existing file.
		f = open(path, 'w') 
		return f

	def _sort_by_score(self, tweet_str, score):
		if score > 0:
			try:
				self.pfile.write(tweet_str + '\n')
			except UnicodeEncodeError:
				self.pfile.write("UNREADABLE TWEET\n")
			self.positive_tweets += 1
		elif score < 0:
			try:
				self.nfile.write(tweet_str + '\n')
			except UnicodeEncodeError:
				self.nfile.write("UNREADABLE TWEET\n")
			self.negative_tweets += 1
		else:
			self.neutral_tweets += 1
			print("Neutral tweet no. {0}".format(self.neutral_tweets))

	def analyze(self, key_words, tweet):
		# Very very naively calculates an attitude score of the given key_words.
		score = 0
		for word in key_words:
			if word in self.positive_set:
				score += 1
			elif word in self.negative_set:
				score -= 1
		self._sort_by_score(tweet, score)

	def display_stats(self):
		total = self.positive_tweets + self.negative_tweets + self.neutral_tweets
		run_time = round(time.time() - self.start_time, 1)
		print("Processing Terminated.")
		print("Total tweets processed: {0}".format(total))
		print("Positive tweets: {0}".format(self.positive_tweets))
		print("Negative tweets: {0}".format(self.negative_tweets))
		print("Neutral tweets: {0}".format(self.neutral_tweets))
		print("Total running time: {0} seconds".format(run_time))

def setup_word_set(path):
	result_set = set()
	with open(path) as f:
		i = 0
		for line in f:
			# Skip first 15 lines - contains citations.
			if i < 15:
				i += 1
				continue
			result_set.add(line.strip())
	return result_set


