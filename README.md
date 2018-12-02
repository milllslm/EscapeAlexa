         ___        ______     ____ _                 _  ___  
        / \ \      / / ___|   / ___| | ___  _   _  __| |/ _ \ 
       / _ \ \ /\ / /\___ \  | |   | |/ _ \| | | |/ _` | (_) |
      / ___ \ V  V /  ___) | | |___| | (_) | |_| | (_| |\__, |
     /_/   \_\_/\_/  |____/   \____|_|\___/ \__,_|\__,_|  /_/ 
 ----------------------------------------------------------------- 


Hi there! Welcome to AWS Cloud9!

To get started, create some files, play with the terminal,
or visit https://docs.aws.amazon.com/console/cloud9/ for our documentation.

Happy coding!

# CS278 Alexa Escape Game

Our final project stemmed from our team's interest Amazon Alexa development, as well as our desire to create an application that could be extended and built upon. After deciding upon an Alexa application, we narrowed down our project options to either a skill based application to teach the user a certain skill, or a more open ended game. While some of the skills we thought about included a Rubiks cube solver and fitness application, none of us had experience with teaching and were not sure how to best go about development and instruction. As for the game, we knew that there were many options that we could pursue, but wanted to be creative with it. After some thought, we decided on an escape game in which the user would have the ability to work their way through a number of rooms by collecting items and interacting with other objects. 
<br/> <br/>

# Development Approach
Amazon has a full suite of resources and documentation for developers to create their own custom skill for Alexa, which did simplify the process a bit. The Alexa skill is composed to two components: the skill interface and skill service. The interface processes the user's speech requests and maps them to intents within the interaction model. Each intent is built around an utterance or work that used to invoke the intent, which then creates a JSON encoded event. The skill service determines what actions to take in response to the JSON event. The service returns a JSON encoded response to the skill interface for processing, which is all handled on the backened through a configured enpoint and Lambda function. The three types of requests are the LaunchRequest, IntentRequest, and SessionEndedRequest. LaunchRequest is sent within the event to the Lambda function when the user invokes the skill. IntentRequest is sent when user interacts with the skill and speech request is mapped to an intent. SessionEndedRequest is sent within event to Lambda function when the session ends.
<br/> <br/>

The skil interface was implemented within the Amazon Alexa developers platform and console. Within the console, we were able to set up the intents and invocations to allow the user to start the game, list out options, and interact with certain items. Once the intents are processed, they are passed to the backend for handling and mapping. Each intent has a registered function that handles the request and updates the state. The code is built on a number of objects, such as Rooms, Edges (doors), Items, and Interactables. 

# Intents
There are a number of intents to interact with the room. Upon the start of the game, the user will be read a description of the room, with imems and edges, or doors. With this information, the user will be able to interact with the items described and try to make it through an edge to the next room. Items picked up will be added to an inventory, and persist throughout the game. 
* Open Game: Play game, start, start game
* Item: Pick up {item}
* Using Item: Use {item} on {edge, interactable}
* Interaction: Interact with {interactable}
* Options: options, what can i do, choices, options please

# Further Work
Because the application is built on individual rooms, we can continue to add complexity to the game through more rooms, objects, and interactables. 




