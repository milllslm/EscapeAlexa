"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at testing push message
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import jsonpickle

# --------------- Class Definitions, idk python very well so weshould move these
# testing sachit
class Edge:
    def __init__(self, name, description, unlocked, destination, validItemsToUnlockSelf):
        self.name = name
        self. description = description
        self.unlocked = unlocked
        self.destination = destination
        self.validItemsToUnlockSelf = validItemsToUnlockSelf
        
    def isUnlocked(self):
        return self.unlocked

class Item: 
    def __init__(self, name, description, unlocked):
        self.name = name
        self. description = description
        self.unlocked = unlocked 
        
    def isUnlocked(self): 
        return self.unlocked

class Interactable:
    def __init__(self, name, description, unlocked, validItemsToUnlockSelf, hiddenItems):
        self.name = name
        self.description = description
        self.unlocked = unlocked
        self.validItemsToUnlockSelf = validItemsToUnlockSelf
        self.hiddenItems = hiddenItems
        
    def isUnlocked(self):
        return self.unlocked
        
    def onInteracted(self): #maybe we pass in what interacted with it?
        #do something, currentRoom.items += hiddenItems, maybe room
        #needs an onInteracted(self, interactable)
        #will need to return a map with :text and :itemsToAdd
        return {"text" : "you interacted with " + self.name + ". Inside you found " + ', '.join(self.hiddenItems),
        "itemsToAdd" : self.hiddenItems}
        
class Room:
    def __init__(self, name, description, edges, items, interactables, unlocked):
        self.name = name
        self.description = description
        self.edges = edges
        self.items = items
        self.interactables = interactables
        self.unlocked = unlocked
        
    def onInteracted(self, interactable):
        interactedMap = interactable.onInteracted()
        for item in interactedMap["itemsToAdd"]:
            for itemInItems in self.items:
                if itemInItems.name is item:
                    itemInItems.unlocked = True
        return interactedMap["text"]
        
        #sample intialization of a room that works in a python repl
##myInteractable = Interactable("interactable", "an interactable", True, [], ["item"])

##myRoom = Room("room", "a room", [], [Item("item", "an item", False)], [myInteractable])

##print(myRoom.name)
##print(myRoom.description)
##print(myRoom.edges[0].name)

##myRoom.edges.append(Edge("edge2", "another edge", True))

#print(myRoom.onInteracted(myInteractable))

#for item in myRoom.items:
#  if item.isUnlocked():
#    print(item.name)
        


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    
    myRoom = Room("room", "a room", [], [Item("item", "an item", False)], [Interactable("interactable", "an interactable", True, [], ["item"])], True)
    session_attributes = {}
    #session_attributes = {"curRoom": myRoom, "inventory": []} #load the room from json or something, curRoom: Room1, inventory: []
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Escape Game. " \
                    "This game will walk you through various rooms in your quest to escape the house. " \
                    "Each room will be described to you, before outlining your possible moves, " \
                    "If you would like to continue say, start game"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please start the game by saying, " \
                    "start game."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Escape Game. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}
    
def create_new_inventory_with_item(itemToPickup, session):
    return {"inventory": session['attributes']['inventory'].append(itemToPickup)}

def first_room_dialogue(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    #+ session['attributes']['curRoom'].name + \
    speech_output = "You have entered, " \
                    "we desperately need a storyboard soon, " \
                    "I am not that creative. " \
                    "At any point during the game, " \
                    "you may say, options, for a full list of available " \
                    "actions you may take."
                    
    reprompt_text = "Didn't catch that what did you say"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def list_options(intent, session):
    """Lists all options for the player to act on
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_output = "I got I got I got I got options, [movement options]" \
                    " [inventory options] [built in alexa help and quit]"
    
    reprompt_text = "Didn't catch that what did you say"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def pickup_item(intent, session):
    "Picks up an item and adds it to the players inventory"
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    if 'Item' in intent['slots']:
        itemToPickup = intent['slots']['Item']['value']
        session_attributes.update(create_new_inventory_with_item(itemToPickup, session))
        speech_output = "You picked up the " + \
                        itemToPickup + \
                        " and added it to your inventory."
        reprompt_text = "You can pick up items by saying, pickup 'item name'"
        
    else:
        speech_output = "That is not a valid item, please try again by saying, pick up and then a valid item"
        reprompt_text = "That is not a valid item, please try again by saying, pick up and then a valid item"
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    #load house(json file or something), gonna need to point session to the room below somehow
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "StartGameIntent":
        return first_room_dialogue(intent, session)
    elif intent_name == "OptionsIntent":
        return list_options(intent, session)
    elif intent_name == "PickupIntent":
        return pickup_item(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
