import random
# Function get_category: Now that we have our user category, we find 10 books
# from the same category in our data file.
def recommendation(user_cat):
    file = open("Classified.txt", 'r', encoding='latin-1')
    lines = file.readlines()
    books = []
    
    for line in lines:
        entries = line.split("\t")
        author = entries[0]
        title = entries[1]
        categories = entries[2:]
        entry = [author, title, categories]
        # if same category as requested, add to books
        for cat in categories:
            print(cat)

            if user_cat in cat:
                books.append(entry)
    file.close()

    # if we couldn't find any in the same category:
    error_strings = ["Sorry, I couldn't find a book suited to your preferences. Could you please try again?\n",
                     "Sorry human, this type of book is too niche for my algorithm. Find something more mainstream:\n",
                     "Dude no one reads these books anymore. Throw something else at me!\n",
                     "Yeah... That's definitely not in our database. Try again!\n"]
    if len(books)== 0:
        return random.choice(error_strings)
    
    else:
        if len(books) >= 5:
            randomBooks = random.sample(books, 5)
        else:
            randomBooks = books
            
    # Return the bot message
    string = ""
    strings1 = ["Based on your preferences, I would recommend:\n",
                "According to our algorithm, you'd love these books:\n",
                "Here are a few books aligned with your niche interests:\n",
                "Yeah... I think I got something for you:\n",
                "Here you go! That's some nice literary taste you got there, by the way.\n"]
    string += random.choice(strings1)
     
    for i in range(len(randomBooks)):
        entry = randomBooks[i]
        string += ("\t"+entry[1]+" by "+entry[0]+"\n")
        
    strings2 = ["Is there an other kind of book that you like?\n",
                "Throw something else at me!\n",
                "Any other ideas of books? Come on, there must be something!\n"]   
    string += random.choice(strings2)
    
    return string

if __name__ == '__main__':
    print(recommendation("Books & Literature"))





