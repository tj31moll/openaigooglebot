from chatterbot.trainers import ListTrainer

trainer = ListTrainer(bot)

conversation = [
    "Hello",
    "Hi there!",
    "How are you?",
    "I'm doing great.",
    "That's good to hear.",
    "Thank you.",
    "You're welcome."
]

trainer.train(conversation)

from chatterbot.trainers import ChatterBotCorpusTrainer

trainer = ChatterBotCorpusTrainer(bot)

trainer.train("chatterbot.corpus.english.greetings",
              "chatterbot.corpus.english.conversations")

from chatterbot.trainers import UbuntuCorpusTrainer

trainer = UbuntuCorpusTrainer(bot)

trainer.train()

from chatterbot.trainers import TwitterTrainer

trainer = TwitterTrainer(bot)

trainer.set_twitter_credentials(
    consumer_key='your_consumer_key',
    consumer_secret='your_consumer_secret',
    access_token='your_access_token',
    access_token_secret='your_access_token_secret'
)

trainer.train()
