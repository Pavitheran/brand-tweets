import pika
import re
import sys

from analyzer import TweetAnalyzer


class TweetProcessor(object):
	"""
	Consumes and analyzes tweets from RabbitMQ to attempt to make
	conclusions about the attitude towards the topic.
	"""
	def __init__(self):
		self.analyzer = TweetAnalyzer()

	def remove_special_chars(self, word):
		if word[-1] == '?' or word[-1] == '.' or word[-1] == '!' or word[-1] == ',':
			word = word[:-1]
		if len(word) > 1 and word[0] == '#':
			word = word[1:]
		return word

	def filter_invalid_words(self, word_list):
		result = []
		# Only want strings containing English language chars.
		alpha = re.compile('^[a-z]+$')
		for word in word_list:
			word = self.remove_special_chars(word).lower()
			match = alpha.match(word)
			if match:
				result.append(match.group(0))
		return result

	def callback(self, ch, method, properties, body):
		# Tweet stream received as byte string.
		tweet_str = body.decode('utf-8')

		# Preprocessing tweets
		tweet_array = tweet_str.split()
		key_words = self.filter_invalid_words(tweet_array)

		self.analyzer.analyze(key_words, tweet_str)


	def start_processing(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(
		               'localhost'))
		channel = connection.channel()

		channel.queue_declare(queue='process_queue')

		channel.basic_consume(
			self.callback, 
			queue='process_queue',
			no_ack=True
			)
		print(" [*] Waiting for messages. To exit press CTRL+C")
		channel.start_consuming()


	def start(self):
		try:
			self.start_processing()
		finally:
			self.analyzer.pfile.close()
			self.analyzer.nfile.close()
			self.analyzer.display_stats()


if __name__ == '__main__':
	TweetProcessor().start()
