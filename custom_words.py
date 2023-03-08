import random

def handle_custom_words(text):
    if text.lower() == "tell me a joke":
        # Define a list of jokes
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the tomato turn red? Because it saw the salad dressing!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "Why did the chicken cross the playground? To get to the other slide!"
        ]
        
        # Select a random joke from the list
        joke = random.choice(jokes)

        # Print the joke
        print(joke)


#def custom_task():
#    # Your custom task code here
#    pass

#def custom_script():
#    # Your custom script code here
#    pass

