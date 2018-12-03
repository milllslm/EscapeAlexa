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
    def __init__(self, name, unlocked):
        self.name = name
        self.unlocked = unlocked 
        
    def isUnlocked(self): 
        return self.unlocked

class Interactable:
    def __init__(self, name, unlocked, validItemsToUnlockSelf, hiddenItems):
        self.name = name
        self.unlocked = unlocked
        self.validItemsToUnlockSelf = validItemsToUnlockSelf
        self.hiddenItems = hiddenItems
        
    def isUnlocked(self):
        return self.unlocked
        
    def onInteracted(self): 
        if not self.hiddenItems:
            endText = "Nothing of note was found inside."
        else:
            endText = "Inside you found a " + ", a ".join(self.hiddenItems[:-2] + [" and a ".join(self.hiddenItems[-2:])])+ "."
        
        textToReturn = "You interacted with " + self.name + ". " + endText
        return {"text" : textToReturn, "itemsToAdd" : self.hiddenItems}

def build_room_description(name, edges, items, interactables):
    name_sentence = "You have entered the " + name + " . "
    edges_sentence = ""
    items_sentence = ""
    interactables_sentence = ""
    if not edges:
        edges_sentence = "There are no escapes from this room."
    else:
        edges_sentence = "You may attempt to move from this room to the " + ", the ".join(edges[:-2] + [" or the ".join(edges[-2:])]) + ". "
    
    available_items = []
    for item in items:
        if item.isUnlocked():
            available_items.append(item)
            
    if not available_items:
        items_sentence = "There remain no available items in this room that you may add to your inventory. "
    else:
        items_sentence = "In this room there is a " + ", a ".join([str(x.name) for x in available_items[:-2]] + [" or a ".join(str(x.name) for x in available_items[-2:])]) + " that may be added to your inventory at this time. "
    if not interactables:
        interactables_sentence = "In terms of interactable objects, there are none."
    else:
        interactables_sentence = "In terms of interactable objects, there is a " + ", a ".join([str(x.name) for x in interactables[:-2]] + [" and a ".join(str(x.name) for x in interactables[-2:])]) + "."
    
    return name_sentence + edges_sentence + items_sentence + interactables_sentence
    
class Room:
    def __init__(self, name, edges, items, interactables, unlocked, validItemsToUnlockSelf):
        self.name = name
        self.edges = edges
        self.items = items
        self.interactables = interactables
        self.unlocked = unlocked
        self.validItemsToUnlockSelf = validItemsToUnlockSelf
        self.description = build_room_description(self.name, self.edges, self.items, self.interactables)
        
    def updateDescription(self):
        self.description = build_room_description(self.name, self.edges, self.items, self.interactables)
    
    def onInteracted(self, interactable):
        interactedMap = interactable.onInteracted()
        for item in interactedMap["itemsToAdd"]:
            for itemInItems in self.items:
                if itemInItems.name.lower() == item:
                    itemInItems.unlocked = True
        
        self.description = build_room_description(self.name, self.edges, self.items, self.interactables)
        return interactedMap["text"]