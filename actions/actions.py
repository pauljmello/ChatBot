# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pathlib import Path
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase

#knowledge = Path("data/TickerNames.txt").read_text().split("\n")

#format = TimeSeries(key=tic, output_format='pandas')
#data = format.get <SOME TIME FRAME>('<TICKER SYMBOL>')

#data[0]

tic = "YJH452CREZ8Z0DC0"
knowledge = Path("data/TickerNames.txt").read_text().split("\n")

class ActionCheckTicker(Action):    # Used to ensure ticker is valid for remaining work
    def name(self) -> Text:
        return "action_check_valid_ticker"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            name = msg['value'].upper()
            if name in knowledge:
                return True
            else:
                return False

CheckTickerValidity = ActionCheckTicker()

class ActionTickerExistence(Action):    # Used for user to find/ensure ticker is valid
    def name(self) -> Text:
        return "action_ticker_existence"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            name = msg['value'].upper()
        if name in knowledge:
            dispatcher.utter_message(template="utter_valid_ticker_true", name = name)
            return []
        else:
            dispatcher.utter_message(template="utter_valid_ticker_false", name = name)
            return []

# Below we account for checking and returning todays High
# -------------------------------------------------------
class ActionCheckHigh(Action):
    def name(self) -> Text:
        return "action_check_todays_high"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            name = msg['value'].upper()
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            highVal = get_ticker_info_adjusted_daily(name, '2. high')
            dispatcher.utter_message(text= f"Todays high for {name} was {highVal}.")
            return []
        else:
            dispatcher.utter_message(template="utter_unfound_ticker_symbol", name = name)
            return []
# ------------------------------------------------------

# Below we account for checking and returning todays Low
# ------------------------------------------------------
class ActionCheckLow(Action):
    def name(self) -> Text:
        return "action_check_todays_low"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            name = msg['value'].upper()
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            lowVal = get_ticker_info_adjusted_daily(name, '3. low')
            dispatcher.utter_message(text= f"Todays low for {name} was {lowVal}.")
            return []
        else:
            dispatcher.utter_message(template="utter_unfound_ticker_symbol", name = name)
            return []
# --------------------------------------------------------

# Below we account for checking and returning todays Open
# --------------------------------------------------------
class ActionCheckOpen(Action):
    def name(self) -> Text:
        return "action_check_todays_open"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            name = msg['value'].upper()
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            val = get_ticker_info_adjusted_daily(name, '1. open')
            dispatcher.utter_message(text= f"Today {name} opened at {val}.")
            return []
        else:
            dispatcher.utter_message(template="utter_unfound_ticker_symbol", name = name)
            return []
# --------------------------------------------------------

# Below we account for checking and returning todays Close
# --------------------------------------------------------
class ActionCheckClose(Action):
    def name(self) -> Text:
        return "action_check_todays_close"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            name = msg['value'].upper()
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            val = get_ticker_info_adjusted_daily(name, '4. close')
            dispatcher.utter_message(text= f"Today {name} closed at {val}.")
            return []
        else:
            dispatcher.utter_message(template="utter_unfound_ticker_symbol", name = name)
            return []
# ------------------------------------------------------------------

# Below we account for checking and returning todays trading Volume
# ------------------------------------------------------------------
class ActionCheckVolume(Action):
    def name(self) -> Text:
        return "action_check_todays_volume"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            name = msg['value'].upper()
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            val = get_ticker_info_adjusted_daily(name, '6. volume')
            dispatcher.utter_message(text= f"Todays traded volume for {name} was {val}.")
            return []
        else:
            dispatcher.utter_message(template="utter_unfound_ticker_symbol", name = name)
            return []
# ------------------------------------------------------

# Inefficent API call, in the future we could save a large chunk of data and pull from local storage instead
# For now this suits our needs because it gives us the ability to make 500 free api calls a day
def get_ticker_info_adjusted_daily(ticker, request):
    TS = TimeSeries(key='YJH452CREZ8Z0DC0', output_format='pandas')
    data = TS.get_daily_adjusted(ticker, outputsize='compact')
    data = data[0]
    data = pd.DataFrame(data)
    val = data[request][0]
    return val

class KnowledgeBase(ActionQueryKnowledgeBase):
    def __init__(self):
        ticker_kb = InMemoryKnowledgeBase("data/TickerInfo.json")
        super().__init__(ticker_kb)