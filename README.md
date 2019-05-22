# Building a LUIS application with a Python client

This tutorial will teach you how to create an application in LUIS and write a simple client in python to consume the application.  
We will leverage prebuilt entities to extract data from user queries in LUIS, and an API from the [MLB](https://www.mlb.com/) to retrieve statistics about the entities LUIS finds.

### Prerequisites

*   Python 3.x
*   [Requests](https://github.com/kennethreitz/requests), a python library for making HTTP requests easily.
*   A [LUIS.ai](http://LUIS.ai) account where to create the sample’s LUIS model.

### Running the sample

If you would like to run the sample, simply clone the repository and run the following command inside the directory:

```
    python client.py
```

# Step 1\. Creating our Model

## Creating a new app

1.  Sign in to the [LUIS portal](https://www.luis.ai).
2.  Select **Create new app**.
3.  In the pop-up dialog, enter the name `Baseball` and keep the default culture, English. You may leave the description blank.
4.  Select **Done**. Next, the app shows the **Dashboard**.
5.  Select **Build** from the top right menu. The **Intent** page is shown.

## Add a prebuilt entity to help with common data type extraction

LUIS provides several prebuilt entities for common data extraction.

1.  Select **Entities** from the left navigation menu.
2.  Select **Add prebuilt entity** button.
3.  Select the `PersonName` entity from the list, then select **Done**.

This entity will help us extract name data from user queries.

## Add custom intents

LUIS uses intents to determine what the query is attempting to ask. We are going to add two custom intents,  
`FindHomeRuns` and `FindBattingAverage`

1.  Select **Intents** from the left navigation menu.
2.  Select **Create new intent** button.
3.  In the pop-up dialog enter the name ‘FindHomeRuns’.
4.  Select **Done**. Next, the app show the **Intents** page with our **FindHomeRuns** Intent added as well as the default **None** Intent.
5.  Repeat steps 2-4 for **FindBattingAverage**

## Add sample utterances to the custom intents

By providing example utterances, you are training LUIS about what kinds of utterances should be predicted for this intent. In order to have functioning predictions, we want about 15 or so sample utterances of varying gramatical structure and accuracy.

To add sample utterances to an intent, do the following:

1.  Select **Intents** from the left navigation menu.
2.  Select the desired intent, in this case **FindHomeRuns**.
3.  Input a sample utterance into the text field and press **Enter**.
4.  You will see the name data from the sample utterance replaced with a `personName` entity.

Repeat these steps for **FindBattingAverage** using the following sample utterances.

Example utterances for **FindHomeRuns**:

*   How many home runs does John Smith have?
*   How many home runs has Mike Trout hit?
*   How many homers does Hanley Ramirez have?
*   ### CAN ADD MORE HERE

Example utterances for **FindBattingAverage**:

*   What is John Smith hitting?
*   What is Mike Trout’s batting average?
*   What is Robinson Cano batting?
*   What is Hanley Ramirez’s average?
*   ### CAN ADD MORE HERE

## Use sample utterances to create patterns

Patterns allow us to improve intent and entity prediction while providing fewer example utterances.  
We can create a pattern from sample utterances by doing the following:

1.  Select **Intents** from the left navigation menu.
2.  Select the desired intent, in this case **FindHomeRuns**.
3.  Select the **Add as pattern** button.
4.  In the pop-up dialog, select **Done**.
5.  Repeat with other desired sample utterances.

## Add example utterances to the None intent

The client application needs to know if an utterance is not meaningful or appropriate for the application. The None intent is added to each application as part of the creation process to determine if an utterance can’t be answered by the client application.

If LUIS returns the None intent for an utterance, your client application can ask if the user wants to end the conversation or give more directions for continuing the conversation.

#### `Do not leave the None intent empty.`

1.  Select **Intents** from the left panel.
2.  Select the **None** intent. Add three utterances that your user might enter but are not relevant to your Human Resources app:

Example utterances:

*   Barking dogs are annoying
*   Order a pizza for me
*   Penguins in the ocean

## Train the app before testing or publishing

Now that we have sample utterances and patterns, we can train our model.

1.  In the top right side of the LUIS website, select the Train button.

2.  Training is complete when you see the green status bar at the top of the website confirming success.

## Publish the app to query from the endpoint

In order to receive a LUIS prediction in a chat bot or other client application, you need to publish the app to the endpoint.

1.  Select **Publish** in the top right navigation.
2.  Select the **Production** slot and the **Publish** button.
3.  Publishing is complete when you see the green status bar at the top of the website confirming success.
4.  Select the endpoints link in the green status bar to go to the Keys and endpoints page. The endpoint URLs are listed at the bottom.
5.  Save the endpoint URL. We will use it in our client.

# 2\. Writing the client

Now that our LUIS application has a trained and published model, we can write an application to leverage it.  
If you don’t have the `requests` python module installed, use the following command:

```
    pip install requests
```

Make sure to include the library in our client.
```python
    import requests
```
We also define two important global variable with the URLS we need. Note in the player_stats URL there are variables for **game_type** (R for regular season or P for postseason) and **season** (year of the desired season).
```python
    luis_url = # The URL endpoint for LUIS
    stats_url = "http://lookup-service-prod.mlb.com/"
    player_info = "json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part="
    player_stats = "json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2017'&player_id="
```
## Using the requests library to get JSON data

Both LUIS and the MLB Stats API return data in the form of JSON. We create the following function to handle this:
```python
    def get_json(url):
        response = requests.get(url)
        try:
            json = response.json()
            return json
        except:
            return {}
```
## Getting a player’s ID

In order to access a player’s statistics via the MLB Stats API, we need a way of turning a player’s name into the corresponding player ID. Fortunately, there is a way we can do that using the MLB’s api.
```python
    def get_player_id(player_name):
        url = stats_url + player_info + "\'" + player_name + "\'"
        json = get_json(url)
        try:
            player_id = json['search_player_all']['queryResults']['row']['player_id']
        except Exception as e:
            player_id = '0'
        finally:
            return player_id
```
## Getting statistics

Now that we can get the player’s ID, we can find any statistics we desire as long as we know the code representing it.  
For the case of Home Runs and Batting averages, the codes are **hr** and **avg**, respectively.
```python
    def get_statistic(player_id, statistic):
        url = stats_url + player_stats + player_id
        json = get_json(url)
        try:
            res = json['sport_hitting_tm']['queryResults']['row'][statistic]
        except Exception as e:
            res = '0'
        finally:
            return res
```
## Client interaction

Our data extracting functions are in place. Now all we need to do is write some Input/Output loops.  
Our main function begins as such:
```python
    def main():
        while True:
            query = input("\nPlease enter your query: \n\n")
            print()
            url = luis_url + query
            json = get_json(url) # response from our LUIS application
```
At this point our LUIS application has processed the user’s query, determining intent and finding entities. We can capture these values like this:
```python
            intent = json['topScoringIntent']['intent']
            player_name = json['entities'][0]['entity'] # The 0 here represents the first entity returned
            player_id = get_player_id(player_name)
```
What happens if the MLB’s api can’t find the player’s ID and player_id is 0? We could create and raise a custom Exception, but it is simpler just to notify the user and continue the loop.
```python
            if (player_id == '0'):
                    print("Couldn't find that player. Please try again.")
                    continue
```
Next we write the logic for handling the proper statistical query based on the User’s intent.
```python
            if (intent == "FindBattingAverage"):
                    avg = get_statistic(player_id,'avg')
                    print("\t" + player_name + " is batting " + avg)
            elif (intent == "FindHomeRuns"):
                    hr = get_statistic(player_id,'hr')
                    print("\t" + player_name + " has " + hr + " home runs")
            else: # intent == None
                    print("\tCouldn't understand your query, to exit press CTRL+C.")
                    continue
```
Because errors are possible if we trying to parce responses that are not valid, we handle any Exceptions raised by those operations at the end, wrapping all the above logic in a try block. The final main function looks like this:
```python
    def main():
        while True:
            query = input("\nPlease enter your query: \n\n")
            print()
            url = luis_url + query
            json = get_json(url) 

            try:
                intent = json['topScoringIntent']['intent']
                player_name = json['entities'][0]['entity']
                player_id = get_player_id(player_name)

                if (player_id == '0'):
                    print("Couldn't find that player. Please try again.")
                    continue

                if (intent == "FindBattingAverage"): # FindBattingAverage
                    avg = get_statistic(player_id,'avg')
                    print("\t" + player_name + " is batting " + avg)
                elif (intent == "FindHomeRuns"): # FindHomeRuns
                    hr = get_statistic(player_id,'hr')
                    print("\t" + player_name + " has " + hr + " home runs")
                else: # None
                    print("\tCouldn't understand your query, to exit press CTRL+C.")
            except Exception as error:
                print(error)

    if __name__ == "__main__":
        main()
```
The last two lines at the end cause the main function to autorun when the python module is invoked.

## 3. Running our client

To run the client, open a command prompt, navigate to the directory where `client.py` is and run

    python client.py

Now you can enter queries and watch as our client uses LUIS and the MLB API to return relevant statistics based on user intent!

    Please enter your query:

    how many home runs does hanley ramirez have this season?

        hanley ramirez has 23 home runs

    Please enter your query:

    what is joey votto batting?

        joey votto is batting .320

## What’s next?

Extending the functionality is easy. Simply update the LUIS app’s intents and add logic for the selection of additional stats. For more information about LUIS, please visit [https://docs.microsoft.com/en-us/azure/cognitive-services/luis/](https://docs.microsoft.com/en-us/azure/cognitive-services/luis/).