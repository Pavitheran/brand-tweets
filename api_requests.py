import argparse
import json
import pika
import sys

from config import *
from twython import TwythonStreamer

"""
Connects to the Twitter Streaming API and tracks a topic passed 
in as a command line argument. 
The relevent tweets are published into a message queue (RabbitMQ) 
for later processing.
"""

class TwitStream(TwythonStreamer):

	def __init__(self, app_key, app_secret, token_key, token_secret):
		super().__init__(app_key, app_secret, token_key, token_secret)
		self.processed_count = 0
		self.connection = None
		self.channel = None
		self.setup_message_queue()

	def setup_message_queue(self):
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(
				'localhost'
				)
			)
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='process_queue')

	def publish_tweet(self, tweet):
		self.channel.basic_publish(
			exchange='',
			routing_key='process_queue',
			body=tweet
			)

	def on_success(self, data):
		if 'text' in data:
			self.processed_count += 1
			tweet = data['text'].encode('utf-8')
			# Send tweets through RabbitMQ for processing
			self.publish_tweet(tweet)

			if self.processed_count % 100 == 0:
				print("{0}th Tweet Processed".format(self.processed_count))

	def on_error(self, status_code, data):
		print(status_code)
		self.connection.close()
		self.disconnect()


def process_cmd_line_args():
	parser = argparse.ArgumentParser(
		description="Analyze a brand's perception on Twitter."
		)
	parser.add_argument(
		'--brand-name',
		dest='topic',
		help='Name of the brand you want to track.'
		)
	args = parser.parse_args()
	return args.topic


def tail_topic():
	topic = process_cmd_line_args()
	# Connect to api using keys from config
	print("Following live Twitter stream...CTRL+C to abort.")
	stream_api = TwitStream(
		CONSUMER_KEY,
		CONSUMER_SECRET,
		ACCESS_TOKEN,
		ACCESS_SECRET
		)
	stream_api.statuses.filter(track=topic)


# GO
if __name__ == '__main__':
	tail_topic()
