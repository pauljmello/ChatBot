# Stock Market Chatbot

### __Purpose__ ###

Most financial websites have a considerable amount of "fat" and "fluff" that can inhibit a common users experience to see the information they desire.  The purpose of this project is to develop a chat bot that is capable of relaying recent stock market information to a user without this extra fluff. In this way we can comb through the data to retrieve only the most relevant pieces a user desires. Specifically, this chat bot is currently able to return the most recent High, Low, Open, Close, and trading volume of any given stock on the NYSE.

### __Contents__ ### 

This bot is capable of understanding a total of 21 user utterances and capable of responding with 21 unique types of messages. Part of these utterances include a small bit of banter that provides the user with a more human like experience. It can also handle a total of 5 multi-turn conversations where a user may ask for different stocks given a goal, or different goals given a stock. This is done by storing recent user messages and saving the extracted entitites for a users goal and stock choice. 

This bot uses Alpha Vantage's API to return the daily values of a stock to the user. Future implementations can expand on the current bot's state inorder to retrieve specific values from a specific date and much more. However, for the scope and goal of this project I am content with its current state. 

### __Capabilities__ ### 

This bot can provide the user with the following information when prompted:

1. Collect and store a users goal and most recent ticker symbol.

2. Todays High, Low, Open, Close, and trading volume individually or aggregated given a user provided stock and goal.

3. Check to see if the user provided ticker symbol is valid on the NYSE.

4. Provide its own capabilities when asked to.

5. Inform the user that it is a bot.

6. Handle multiturn conversation when prompted with ambiguous ticker symbols or ambiguous stock goals.

### __Implemented Conversation Flows__ ### 

Simple Example:

User: Hello
Bot: Hey! How are you?
User: Good thank you! 
Bot: I'm so glad to hear that! What can I help you with?
User: I am looking for information about a stock.
Bot: Sure thing, what stock would you like to know about?
User: Tell me whats going on with AAPL today.
Bot: < Will list todays Open, High, Low, Close, and Volume for AAPL >
User: What about TSLA?
Bot: < Will list todays Open, High, Low, Close, and Volume for TSLA >
User: Thank you!
Bot: Goodbye!

Multiturn Example:

User: hi
Bot: Hey! How are you?
User: im sad and tired
Bot: I'm sorry to hear that. WHow may I be of assistance?
User: idk what can you do?
Bot: < Bot will list its abilities with example commands >
User: Is XOM a valid stock?
Bot: Yes, XOM is a valid ticker symbol.
User: then what was its closing price?
Bot: Today XOM closed at < closing price >
User: Where did it open? 
Bot: Today XOM opened at < opening price >
User: QCOM
Bot: What would you like to know about QCOM?
User: its volume traded
Bot: Todays traded volume for QCOM was < traded volume >
User: thank you
Bot: Goodbye!

These examples illustrate the types of conversations flows implemented in this chat bot.

### __Notes__ ###

In order to run this program one must install all the packages in the requirments.txt. This will ensure that the proper packages are loaded. Additionally, it is crucial to note that the chatbot requires a user to know the ticker symbol and provide it to the bot in all capital letters, just as one would see on the stock market. This is because their are many ticker symbols which overlap with english words. 