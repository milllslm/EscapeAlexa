"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at testing push message
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import jsonpickle
import jsonpickle.tags as tags
import jsonpickle.unpickler as unpickler
import jsonpickle.util as util

import models.Ed
        
#ITEMS
paperclip = Item("paperclip", False)
red_key = Item("red key", False)
eyeball = Item("eyeball", False)
crowbar = Item("crowbar", False)
flashlight = Item("flashlight", False)
hammer = Item("hammer", False)
blue_key = Item("blue key", False)
screwdriver = Item("screwdriver", False)
glove = Item("glove", False)
skull = Item("skull", False)
fingerprint = Item("fingerprint", False)

#INTERACTABLES
toilet_paper = Interactable("toilet paper", True, [], ["paperclip"])
lockbox = Interactable("lockbox", False, ["paperclip"], ["red key"])
sink = Interactable("sink", True, [], ["eyeball"])
bathtub = Interactable("bathtub", True, [], ["crowbar"])
eyeless_painting = Interactable("eyeless painting", False, ["eyeball"], ["flashlight"])
cracked_painting = Interactable("cracked painting", False, ["crowbar"], ["hammer"])
shoe_box = Interactable("shoe box", True, [], [])
skull_chest = Interactable("skull chest", False, ["skull"], ["fingerprint"])
hollow_wall = Interactable("hollow wall", False, ["hammer"], ["screwdriver"])
oven = Interactable("oven", False, ["flashlight"], ["glove", "blue key"])
bookshelf = Interactable("bookshelf", True, [], ["skull"])
loosely_screwed_floorboard = Interactable("loosely screwed floorboard", False, ["screwdriver"], [])


#ROOMS
bathroom = Room("bathroom", ["hallway"], [red_key, paperclip, eyeball, crowbar], [toilet_paper, lockbox, bathtub, sink], True, [])
hallway = Room("hallway", ["bathroom", "attic", "library"], [flashlight, hammer], [eyeless_painting, cracked_painting], False, ["red key"])
attic = Room("attic", ["hallway", "kitchen"], [fingerprint], [shoe_box, skull_chest], True, [])
kitchen = Room("kitchen", ["attic"], [glove, blue_key, screwdriver], [oven, hollow_wall], True, [])
library = Room("library", ["hallway", "outside"], [skull], [bookshelf, loosely_screwed_floorboard], False, ["blue key"])
outside = Room("outside", ["library"], [], [], False, ["fingerprint"])

RoomNameObjMap = {"bathroom" : bathroom, "hallway": hallway, "attic": attic, "kitchen": kitchen, "library": library, "outside": outside}

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
    
def list_inventory_options(priorInventory):
    """Lists inventory options for the player in the current context"""
    if not priorInventory:
        return "no items"
    else:
        return ", ".join(priorInventory[:-2] + [" and ".join(priorInventory[-2:])])

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global myRoom
    session_attributes = {}
    session_attributes = {"curRoom": jsonpickle.encode(bathroom), "inventory": [], "roomNameObjMap": jsonpickle.encode(RoomNameObjMap)} #load the room from json or something, curRoom: Room1, inventory: []
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Escape Game. " \
                    "This game will walk you through various rooms in your quest to escape the house. " \
                    "Each room will be described to you, you may say, options, at any point to have your options read to you, " \
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
    speech_output = "Thank you for playing the Alexa Escape Game. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

    
def create_new_inventory_with_item(itemToPickup, priorInventory):
    priorInventory.append(itemToPickup)
    return {"inventory": priorInventory}

def first_room_dialogue(intent, session):
    return recap_handler(intent, session)
        
def recap_handler(intent, session):
    """Repeats the current room description """
    card_title = intent['name']
    
    session_attributes = {}
    session_attributes = session['attributes']
    curRoom = jsonpickle.decode(session_attributes['curRoom'], classes=(Room, Interactable, Item))
    
    
    should_end_session = False
    
    speech_output = curRoom.description
                    
    reprompt_text = "Didn't catch that what did you say"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def list_options(intent, session):
    """Lists all options for the player to act on
    """
    card_title = intent['name']
    session_attributes = session['attributes']
    if not session_attributes['inventory']:
        priorInventory = []
    else:
        priorInventory = session_attributes['inventory']
        
    should_end_session = False
    inventory_options = ""
    inventory_options = list_inventory_options(priorInventory)
    built_in_alexa_options = "To quit the game say, stop."
    
    speech_output = "You may enter an adjacent room by saying, move to, " \
    "and then the name of an available edge. You may add any available item to your" \
    " inventory by saying, pick up, and then the name of an available item. "+ \
    "You may interact with any interactable in the given room by saying, interact with," \
    "and then a valid interactable. Lastly, you may try and use an item by saying, use " \
    "name-of-item on name-of-interactable-or-edge. Your inventory contains " + \
    inventory_options + ". For a recap of the room you are in say, room recap. " + built_in_alexa_options
    
    
    reprompt_text = "Didn't catch that what did you say"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def pickup_item(intent, session):
    "Picks up an item and adds it to the players inventory"
    #TODO: error when picking up item, wont remove it from list of room.items
    card_title = intent['name']
    session_attributes = session['attributes']
    curRoom = jsonpickle.decode(session_attributes['curRoom'], classes=(Room, Interactable, Item))
    if not session_attributes['inventory']:
        priorInventory = []
    else:
        priorInventory = session_attributes['inventory']
    should_end_session = False
    speech_output = ""
    reprompt_text = "I didn't quite catch that, please try again."
    
    
    if 'Item' in intent['slots']:
        try:
            itemToPickup = intent['slots']['Item']['value']
            for item in curRoom.items:
                if item.name.lower() == itemToPickup.lower() and item.isUnlocked():
                    session_attributes.update(create_new_inventory_with_item(itemToPickup, priorInventory))
                    curRoom.items = [x for x in curRoom.items if  itemToPickup.lower() != x.name.lower()]
                    curRoom.updateDescription()
                    newKeyVal = {curRoom.name: curRoom}
                    oldRoomNameObjMap = jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))
                    oldRoomNameObjMap.update(newKeyVal)
                    session_attributes.update({'roomNameObjMap': jsonpickle.encode(oldRoomNameObjMap)})
                    session_attributes.update({'curRoom': jsonpickle.encode(curRoom)})
                    speech_output = "You picked up the " + \
                            itemToPickup + \
                            " and added it to your inventory."
                    reprompt_text = "You can pick up items by saying, pickup 'item name'"
                    break
    
            if not speech_output:
                speech_output = "You tried to pick up an item that either wasn't in this room or was not yet unlocked, try again."
                reprompt_text = "That is not a valid item, please try again by saying, pick up and then a valid item"
        except KeyError:
            speech_output = "Alexa couldn't identify the item you were trying to pick up, please try again."
    else:
        speech_output = "That is not a valid item, please try again by saying, pick up and then a valid item"
        reprompt_text = "That is not a valid item, please try again by saying, pick up and then a valid item"
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    

def interact_handler(intent, session):
    "Interact with an interactable and resultant effects"
    card_title = intent['name']
    session_attributes = session['attributes']
    curRoom = jsonpickle.decode(session_attributes['curRoom'], classes=(Room, Interactable, Item))
    
    should_end_session = False
    reprompt_text = "That is not a valid interactable, please try again by saying, interact with, and then a valid interactable"

    
    if 'Interactable' in intent['slots']:
        try:
            thingToInteractWith = intent['slots']['Interactable']['value']
            interactedObject = None
            for interactable in curRoom.interactables:
                if thingToInteractWith.lower() == interactable.name.lower():
                    interactedObject = interactable
            if not interactedObject:
                speech_output = "That is not a valid interactable, please try again by saying, interact with, and then a valid interactable"
            elif not interactedObject.unlocked:
                speech_output = "The interactable is currently locked, please try using an item on it."
            else:
                speech_output = curRoom.onInteracted(interactedObject)
        except KeyError:
            speech_output = "Alexa couldn't identify the room you were trying to enter, please try again."
    else:
        speech_output = "That is not a valid interactable, please try again by saying, interact with, and then a valid interactable"
    session_attributes.update({'curRoom': jsonpickle.encode(curRoom)})
    newKeyVal = {curRoom.name: curRoom}
    oldRoomNameObjMap = jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))
    oldRoomNameObjMap.update(newKeyVal)
    session_attributes.update({'roomNameObjMap': jsonpickle.encode(oldRoomNameObjMap)})
                
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def move_rooms(intent, session):
    """ Move into a new room """
    card_title = intent['name']
    session_attributes = session['attributes']
    curRoom = jsonpickle.decode(session_attributes['curRoom'], classes=(Room, Interactable, Item))
    should_end_session = False
    reprompt_text = "You are not able to enter that room from here, either the room is locked or is not accessible from this one."
    room_names_list_ish = jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))
    room_names_list = room_names_list_ish.keys()
    
    if 'Edge' in intent['slots']:
        try:
            roomToEnter = intent['slots']['Edge']['value']
            if roomToEnter not in room_names_list:
                speech_output = "You are trying to move into a room that does not exist."
            elif not jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))[roomToEnter].unlocked: 
                speech_output = "I'm sorry, this room is currently locked, try using an item on it!"        
            elif roomToEnter not in curRoom.edges:
                speech_output = "You are not able to enter that room from here."
            else:
                #its a valid room, lets move
                curRoom = jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))[roomToEnter]
                session_attributes.update({'curRoom': jsonpickle.encode(curRoom)})
                if curRoom.name == "outside":
                    speech_output = "It's over you won congrats go home."
                    should_end_session = True
                else:
                    speech_output = curRoom.description
        except KeyError:
            speech_output = "Alexa couldn't identify the room you were trying to enter, please try again."
    else:
        speech_output = "That is not a valid room to enter, please try again by saying, move to the , and then the room name"
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
            
def use_handler(intent, session):
    """ Use an item on an interactable or an edge"""
    card_title = intent['name']
    session_attributes = session['attributes']
    curRoom = jsonpickle.decode(session_attributes['curRoom'], classes=(Room, Interactable, Item))
    if not session_attributes['inventory']:
        priorInventory = []
    else:
        priorInventory = session_attributes['inventory']
    should_end_session = False
    reprompt_text = "Not sure what you were trying to do there, try again."
    
    if 'UsedOn' in intent['slots'] and 'Item' in intent['slots']:
        #check for valid items and valid usedon, then do the action
        try:
            usedOnName = intent['slots']['UsedOn']['value']
            itemName = intent['slots']['Item']['value']
            if itemName not in priorInventory:
                speech_output = "You tried using an item that does not exist in your inventory, try again please."
            else:
                oldRoomNameObjMap = jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))
                room_names_list = oldRoomNameObjMap.keys()
                if usedOnName in room_names_list:
                    #they tried using item on a room, see if its valid from here
                    if usedOnName in curRoom.edges:
                        #the room is within striking distance of this current room, check if item works on it
                        nextRoom = jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))[usedOnName]
                        if itemName in nextRoom.validItemsToUnlockSelf:
                            #unlock that bad boy
                            nextRoom.unlocked = True
                            #need to update with the new key value pair
                            newKeyVal = {usedOnName: nextRoom}
                            oldRoomNameObjMap.update(newKeyVal)
                            session_attributes.update({'roomNameObjMap': jsonpickle.encode(oldRoomNameObjMap)})
                            speech_output = "You successfully used the " + itemName + " to unlock the " + usedOnName + ", you may now enter that room."
                        else:
                            #this item doesnt work with this room
                            speech_output = "The item you are using does not work on the room you are trying it on, try again."
                    else:
                        #desired room is not within striking distance
                        speech_output = "You are trying to use your item on a room that is not accessible from the one you are currently in, try moving!"
                else:
                    #they tried using item on an interactable, see if its valid in given room then with given item
                    interactedObject = None
                    for interactable in curRoom.interactables:
                        if usedOnName.lower() == interactable.name.lower():
                            interactedObject = interactable
                    if not interactedObject:
                        speech_output = "The interactable that you are trying to use your item on is not in the current room."
                    else:
                        #valid item, valid interactable, check if they match up
                        if itemName in interactedObject.validItemsToUnlockSelf:
                            #unlock that bad boy
                            interactedObject.unlocked = True
                            session_attributes.update({'curRoom': jsonpickle.encode(curRoom)})
                            newKeyVal = {curRoom.name: curRoom}
                            oldRoomNameObjMap = jsonpickle.decode(session_attributes['roomNameObjMap'], classes=(Room, Interactable, Item))
                            oldRoomNameObjMap.update(newKeyVal)
                            session_attributes.update({'roomNameObjMap': jsonpickle.encode(oldRoomNameObjMap)})
                            speech_output = "You successfully used the " + itemName + " to unlock the " + usedOnName + ", you may now interact with it."
                        else:
                            speech_output = "The item you are using is not valid for unlocking the interactable in question, try again."
        except KeyError:
            speech_output = "Alexa couldn't identify the item you were trying to use or whatever you were trying to use it on, please try again."
    else:
        speech_output = "You either tried to use an item that does not exist or tried to use said item on an interactable or edge that does not exist."
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

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
    if intent_name == "StartGameIntent":
        return first_room_dialogue(intent, session)
    elif intent_name == "OptionsIntent":
        return list_options(intent, session)
    elif intent_name == "InteractIntent":
        return interact_handler(intent, session)
    elif intent_name == "PickupIntent":
        return pickup_item(intent, session)
    elif intent_name == "MoveIntent":
        return move_rooms(intent, session)
    elif intent_name == "UseIntent":
        return use_handler(intent, session)
    elif intent_name == "RoomRecapIntent":
        return recap_handler(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return list_options(intent, session)
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
