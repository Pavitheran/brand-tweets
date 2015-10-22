# Brand Tweets

Tail your favourite brand/topic on twitter in real-time to find out how the community feels about it.

## Installation

1. Clone this repository.
2. Download and install RabbitMQ [Here.](https://www.rabbitmq.com/download.html)

## Usage

1. Run api_requests.py with option '--brand-name' set to the topic you want to tail.
2. Run tweet_processor.py
3. Hit CTRL+C to stop the tweet_processor and see topic stats.
4. You can also check the results/ folder to view the original tweets based on classification.

Example:

    First commandline window:

    $ python api_requests.py --brand-name=FIFA

    Second commandline window:

    $ python tweet_processor.py

## Contributing

1. Fork it!
2. Submit a pull request :)
