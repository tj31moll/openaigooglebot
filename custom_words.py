import random

words = {
    "tell me a joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "Why did the chicken cross the playground? To get to the other slide!",
    ]
}


def handle_custom_words(text):
    if text.lower() in words:
        # Select a random response from the list of responses
        response = random.choice(words[text.lower()])
        print(response)
        return True
    return False


#def custom_task():
#    # Your custom task code here
#    pass

#def custom_script():
#    # Your custom script code here
#    pass

