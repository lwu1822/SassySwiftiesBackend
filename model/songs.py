import random

song_data = []
song_list = [
    "Tim McGraw"
    "Picture to Burn",
    "Teardrops on My Guitar",
    "A Place in This World",
    "Cold as You",
    "The Outside",
    "Tied Together with a Smile",
    "Stay Beautiful",
    "Shouldve Said No",
    "Marys Song (Oh My My My)",
    "Our Song",
    "I'd Lie",
    "Im Only Me When Im with You",
    "Invisible",
    "A Perfectly Good Heart",
    "Fearless",
    "Fifteen",
    "Love Story",
    "Hey Stephen",
    "White Horse",
    "You Belong with Me",
    "Breathe",
    "Tell Me Why",
    "Youre Not Sorry",
    "The Way I Loved You",
    "Forever & Always",
    "The Best Day",
    "Change",
    "Beautiful Eyes (Japanese edition)",
    "Umbrella (Australian iTunes Store Deluxe edition)",
    "Jump Then Fall (Platinum edition)",
    "Untouchable (Platinum edition)"
    "Come in with the Rain (Platinum edition)",
    "Superstar (Platinum edition)",
    "The Other Side of the Door (Platinum edition)",
    "Mine",
    "Sparks Fly",
    "Back to December",
    "Speak Now",
    "Dear John",
    "Mean",
    "The Story of Us",
    "Never Grow Up",
    "Enchanted",
    "Better than Revenge",
    "Innocent",
    "Haunted",
    "Last Kiss",
    "Long Live",
    "Ours (Bonus Track)",
    "If This Was a Movie (Bonus Track)",
    "Superman (Bonus Track)",
    "State of Grace",
    "Red",
    "Treacherous",
    "I Knew You Were Trouble",
    "All Too Well",
    "22",
    "I Almost Do",
    "We Are Never Ever Getting Back Together",
    "Stay Stay Stay",
    "The Last Time (featuring Gary Lightbody)",
    "Holy Ground",
    "Sad Beautiful Tragic",
    "The Lucky One",
    "Everything Has Changed (featuring Ed Sheeran)",
    "Starlight",
    "Begin Again",
    "The Moment I Knew",
    "Come Back… Be Here",
    "Girl at Home",
    "Welcome to New York",
    "Blank Space",
    "Style",
    "Out of the Woods",
    "All You Had to Do Was Stay",
    "Shake It Off",
    "I Wish You Would",
    "Bad Blood",
    "Wildest Dreams",
    "How You Get the Girl",
    "This Love",
    "I Know Places",
    "Clean",
    "Wonderland",
    "You Are in Love",
    "New Romantics",
    "…Ready for It?",
    "End Game (featuring Ed Sheeran and Future)",
    "I Did Something Bad",
    "Dont Blame Me",
    "Delicate",
    "Look What You Made Me Do",
    "So It Goes…",
    "Gorgeous",
    "Getaway Car",
    "King of My Heart",
    "Dancing with Our Hands Tied",
    "Dress",
    "This Is Why We Cant Have Nice Things",
    "Call It What You Want",
    "New Years Day",
    "I Forgot That You Existed",
    "Cruel Summer",
    "Lover",
    "The Man",
    "The Archer",
    "I Think He Knows",
    "Miss Americana & The Heartbreak Prince",
    "Paper Rings",
    "Cornelia Street",
    "Death By A Thousand Cuts"
    "London Boy",
    "Soon Youll Get Better Ft. Dixie Chicks",
    "False God",
    "You Need to Calm Down",
    "Afterglow",
    "ME! Ft. Brendon Urie",
    "Its Nice to Have a Friend",
    "Daylight",
    "The 1",
    "Cardigan",
    "The Last Great American Dynasty",
    "Exile Ft. Bon Iver",
    "My Tears Ricochet",
    "Mirrorball",
    "Seven",
    "August",
    "This is Me Trying",
    "Illicit Affairs",
    "Invisible String",
    "Mad Woman",
    "Epiphany",
    "Betty",
    "Peace",
    "Hoax",
    "The Lakes",
    "willow",
    "champagne problems",
    "gold rush",
    "tis the damn season",
    "tolerate it",
    "no body, no crime feat. HAIM",
    "happiness",
    "dorothea",
    "coney island feat. The National",
    "ivy",
    "cowboy like me",
    "long story short",
    "marjorie",
    "closure",
    "evermore feat. Bon Iver",
    "right where you left me",
    "its time to go",
    "Fearless (Taylors Version)",
    "Fifteen (Taylors Version)",
    "Love Story (Taylors Version)",
    "Hey Stephen (Taylors Version)",
    "White Horse (Taylors Version)",
    "You Belong with Me (Taylors Version)",
    "Breathe (Ft. Colbie Caillat) (Taylors Version)",
    "Youre Not Sorry (Taylors Version)",
    "The Way I Loved You (Taylors Version)",
    "Forever & Always (Taylors Version)",
    "The Best Day (Taylors Version)",
    "Change (Taylors Version)",
    "Jump Then Fall (Taylors Version)",
    "Untouchable (Taylors Version)",
    "Forever & Always (Piano Version) (Taylors Version)",
    "Come In With the Rain (Taylors Version)",
    "SuperStar (Taylors Version)",
    "The Other Side of the Door (Taylors Version)",
    "Today Was a Fairytale (Taylors Version)",
    "You All Over Me (From The Vault) Ft. Maren Morris",
    "Mr. Perfectly Fine (From The Vault)",
    "We Were Happy (From The Vault)",
    "Thats When (From The Vault) Ft. Keith Urban",
    "Dont You (From The Vault)",
    "Bye Bye Baby (From The Vault)",
    "Love Story (Taylors Version) Elvira Remix", 
    "State of Grace (Taylors Version)",
    "Red (Taylors Version)",
    "Treacherous (Taylors Version)",
    "I Knew You Were Trouble (Taylors Version)",
    'All Too Well (Taylors Version)',
    "22 (Taylors Version)",
    "I Almost Do (Taylors Version)",
    "We Are Never Ever Getting Back Together (Taylors Version)",
    "Stay Stay Stay (Taylors Version)",
    "The Last Time (Taylors Version) (featuring Gary Lightbody)",
    "Holy Ground (Taylors Version)",
    "Sad Beautiful Tragic (Taylors Version)",
    "The Lucky One (Taylors Version)",
    "Everything Has Changed (Taylors Version) (featuring Ed Sheeran)",
    "Starlight (Taylors Version)",
    "Begin Again (Taylors Version)",
    "The Moment I Knew (Taylors Version)",
    "Come Back… Be Here (Taylors Version)",
    "Girl at Home (Taylors Version)",
    "Here (Taylors Version)",
    "Ronan (Taylors Version)",
    "Better Man (Taylors Version) (From the Vault)",
    "Nothing New Ft. Phoebe Bridges (Taylors Version) (From the Vault)",
    "Babe (Taylors Version) (From the Vault)",
    "Message in a Bottle (Taylors Version) (From the Vault)",
    "I Bet You Think About Me Ft. Chris Stapleton (Taylors Version) (From the Vault)",
    "Forever Winter (Taylors Version) (From the Vault)",
    "Run Ft. Ed Sheeran (Taylors Version) (From the Vault)",
    "The Very First Night (Taylors Version) (From the Vault)",
    "All Too Well (10-minute version) (Taylors Version) (From the Vault)"
    "Lavender Haze",
    "Maroon",
    "Anti-Hero",
    "Snow On The Beach",
    "Youre On Your Own, Kid",
    "Midnight Rain",
    "Question…?",
    "Vigilante Sh*t",
    "Bejeweled",
    "Labyrinth",
    "Karma",
    "Sweet Nothing",
    "Mastermind",
    "The Great War",
    "Bigger Than The Whole Sky",
    "Paris",
    "High Infidelity",
    "Glitch",
    "Wouldve, Shouldve, Couldve",
    "Dear Reader",
]

# Initialize jokes
def initSongs():
    # setup jokes into a dictionary with id, joke, haha, boohoo
    item_id = 0
    for item in song_list:
        song_data.append({"id": item_id, "song": item, "like": 0, "dislike": 0})
        item_id += 1
    # prime some haha responses
    for i in range(10):
        id = getRandomSong()['id']
        addSongLike(id)
    # prime some haha responses
    for i in range(5):
        id = getRandomSong()['id']
        addSongDislike(id)
        
# Return all jokes from jokes_data
def getSongs():
    return(song_data)

# Joke getter
def getSong(id):
    return(song_data[id])

# Return random joke from jokes_data
def getRandomSong():
    return(random.choice(song_data))

# Liked joke
def favoriteSong():
    best = 0
    bestID = -1
    for song in getSongs():
        if song['like'] > best:
            best = song['like']
            bestID = song['id']
    return song_data[bestID]
    
# Jeered joke
def dislikeSong():
    worst = 0
    worstID = -1
    for song in getSongs():
        if song['dislike'] > worst:
            worst = song['dislike']
            worstID = song['id']
    return song_data[worstID]

# Add to haha for requested id
def addSongLike(id):
    song_data[id]['like'] = song_data[id]['like'] + 1
    return song_data[id]['like']

# Add to boohoo for requested id
def addSongDislike(id):
    song_data[id]['dislike'] = song_data[id]['dislike'] + 1
    return song_data[id]['dislike']

# Pretty Print joke
def printSong(song):
    print(song['id'], song['song'], "\n", "like:", song['like'], "\n", "dislike:", song['dislike'], "\n")

# Number of jokes
def countSongs():
    return len(song_data)

# Test Joke Model
if __name__ == "__main__": 
    initSongs()  # initialize jokes
    
    # Most likes and most jeered
    best = favoriteSong()
    print("Most liked", best['like'])
    printSong(best)
    worst = dislikeSong()
    print("Most disliked", worst['dislike'])
    printSong(worst)
    
    # Random joke
    print("Random song")
    printSong(getRandomSong())
    
    # Count of Jokes
    print("Song Count: " + str(countSongs()))