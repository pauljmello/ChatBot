# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from alpha_vantage.timeseries import TimeSeries
from pathlib import Path
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase

#knowledge = Path("data/TickerNames.txt").read_text().split("\n")
#tic = "YJH452CREZ8Z0DC0"

#format = TimeSeries(key=tic, output_format='pandas')
#data = format.get <SOME TIME FRAME>('<TICKER SYMBOL>')

#data[0]

class ActionCheckTickerExistence(Action):

    def name(self) -> Text:
        return "action_check_ticker_existence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        knowledge = Path("data/TickerNames.txt").read_text().split("\n")
        for msg in tracker.latest_message['entities']:
            print(tracker.latest_message)
            tic_name = msg['value'].upper()
            if tic_name in knowledge:
                dispatcher.utter_message(template="utter_valid_ticker_true", name= tic_name)
                return []
            else:
                dispatcher.utter_message(template="utter_valid_ticker_false", name= tic_name)
                return []
        return []

class KnowledgeBase(ActionQueryKnowledgeBase):
    def __init__(self):
        ticker_kb = InMemoryKnowledgeBase("data/TickerInfo.json")
        super().__init__(ticker_kb)