import json
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pathlib import Path
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet

tic = "YJH452CREZ8Z0DC0"
knowledge = Path("data/TickerNames.txt").read_text().split("\n")

class ActionCheckTicker(Action):    # Returns whether ticker is valid (present in NYSE stock exchange)
    def name(self) -> Text:
        return "action_check_valid_ticker"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        if name in knowledge:
            return True
        else:
            return False

CheckTickerValidity = ActionCheckTicker()

class ActionTickerExistence(Action):    # Used to return statement to user on ticker validity
    def name(self) -> Text:
        return "action_ticker_existence"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            dispatcher.utter_message(response="utter_valid_ticker_true", name = name)
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_valid_ticker_false", name = name)
            return []

# Below we account for checking and returning todays High
# -------------------------------------------------------
class ActionCheckHigh(Action):
    def name(self) -> Text:
        return "action_check_todays_high"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            highVal = get_ticker_info_adjusted_daily(name, '2. high')
            dispatcher.utter_message(text= f"Todays high for {name} was {highVal}.")
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_unfound_ticker_symbol", name = name)
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
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            lowVal = get_ticker_info_adjusted_daily(name, '3. low')
            dispatcher.utter_message(text= f"Todays low for {name} was {lowVal}")
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_unfound_ticker_symbol", name = name)
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
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            openVal = get_ticker_info_adjusted_daily(name, '1. open')
            dispatcher.utter_message(text= f"Today {name} opened at {openVal}")
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_unfound_ticker_symbol", name = name)
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
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            closeVal = get_ticker_info_adjusted_daily(name, '4. close')
            dispatcher.utter_message(text= f"Today {name} closed at {closeVal}")
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_unfound_ticker_symbol", name = name)
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
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            Valume = get_ticker_info_adjusted_daily(name, '6. volume')
            dispatcher.utter_message(text= f"Todays traded volume for {name} was {Valume}")
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_unfound_ticker_symbol", name = name)
            return []
# -----------------------------------------------------------------

# Below we account for checking and returning todays trading Volume
# ------------------------------------------------------------------
class ActionRetrieveTotalDailyAdjusted(Action):
    def name(self) -> Text:
        return "action_check_todays_ticker_total_adjusted"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            data = get_ticker_info_adjusted_daily_total(name)
            open = data['1. open'][0]
            high = data['2. high'][0]
            low = data['3. low'][0]
            close = data['4. close'][0]
            volume = data['6. volume'][0]
            dispatcher.utter_message(text= f"Todays values for {name} are as follows: \nOpen:\t{open} \nHigh:\t{high} \nLow:\t{low} \nClose:\t{close} \nVolume:\t{volume}")
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_unfound_ticker_symbol", name = name)
            return []
# -----------------------------------------------------------------

# Below we account for ambiguous statements given a ticker
# ------------------------------------------------------------------
class ActionAmbiguousStatementPurpose(Action):
    def name(self) -> Text:
        return "action_ambiguous_purpose_statement"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = next(tracker.get_latest_entity_values("ticker_symbol"), None) or tracker.get_slot("ticker_symbol")
        goal = next(tracker.get_latest_entity_values("user_stock_information_goal"), None) or tracker.get_slot("user_stock_information_goal")
        SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", open)
        if (CheckTickerValidity.run(dispatcher, tracker, domain)):
            dispatcher.utter_message(text= f"What would you like to know about {name}?")
            return [SlotSet("ticker_symbol", name), SlotSet("user_stock_information_goal", goal)]
        else:
            dispatcher.utter_message(response="utter_unfound_ticker_symbol", name = name)
            return []
# -----------------------------------------------------------------

# Inefficent API call, in the future we could save a large chunk of data and pull from local storage instead
# For now this suits our needs because it gives us the ability to make 500 free api calls a day
def get_ticker_info_adjusted_daily(ticker, request):
    data = get_Data(ticker)
    val = data[request][0]
    return val

def get_ticker_info_adjusted_daily_total(ticker):
    data = get_Data(ticker)
    return data

def get_Data(ticker):
    TS = TimeSeries(key=tic, output_format='pandas')
    data = TS.get_daily_adjusted(ticker, outputsize='compact')
    data = data[0]
    data = pd.DataFrame(data)
    return data

class KnowledgeBase(ActionQueryKnowledgeBase):
    def __init__(self):
        ticker_kb = InMemoryKnowledgeBase("data/TickerInfo.json")
        super().__init__(ticker_kb)