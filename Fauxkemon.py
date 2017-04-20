# Final Project
# Oscar Alba
# Lyndsay Hackett
# Kevin Hendershott
# Jennifer Engblom
import random
import urllib
import tempfile

dirThisModule = os.path.dirname(__file__)  #Determine path to this module to simplify other path declarations.


def getOS():
  os = ""
  ver = sys.platform.lower()
  ver = java.lang.System.getProperty("os.name").lower()
  if ver.startswith('mac'):
    os = "mac"
  if ver.startswith('win'):
    os = "win"
  return os

def getMedia(mediaType, fileName):
  suffix = ""
  if mediaType == "img":
    suffix = ".png"
  else:
    suffix = ".wav"

  if getOS() == "win":
   #windows
    #tempPath = "C://Windows//Temp//" + fileName + suffix
    mediaPath = os.path.join(dirThisModule, "media", fileName + suffix)
  else:
    #mac/linux
    #tempPath = tempfile.gettempdir() + fileName + suffix
    mediaPath = os.path.join(dirThisModule, "media", fileName + suffix)
       
  #url = "https://github.com/NoChute/fauxkemon/blob/master/" + fileName + suffix + "?raw=true"
  #data = urllib.urlretrieve(url, tempPath)
  #data = urllib.urlretrieve(url, mediaPath)
     
  if mediaType == "img":
    myMedia = makePicture(mediaPath)
  else:
    myMedia = makeSound(mediaPath)
  return myMedia


#Sound Files
introTheme = getMedia(".wav" , "intro")
viridian = getMedia(".wav" , "ViridiaForest")
battleSong = getMedia(".wav" , "battle")


#Adventure style video game based on Pokemon


def game():
  #open the map for the player
  play(introTheme)
  m = Map("Forest.png")
  intro()
  instructions()
  stopPlaying(introTheme)
  play(viridian)
  initUser()
  #This is a list for the coordinates for the boss encounter
  boss = [(176, 160), (160, 160), (192, 160)]
  #This is a list for the coordinates for the lab encounter
  lab = [(560,992), (576,992), (544,992)]
  #while the game has not been won or lost, run through the whole thing.
  while true:
    x = requestString("Your move?")
    if x == "help":
      instructions()
    elif x == "exit":
      leave()
    elif x == 'inventory':
      #showInformation("Your pokemon are: " + inventory)
      show(getMedia("img", "starters"))
    else:
      m.movePlayer(x)
      
      #if the player is at the boss's door and they move north, this will take them into the boss encounter.
      if (tuple(m.getPlayerLocation()) in boss) and ("n" in x.lower()):
        showInformation("I'm glad to see you finally made it! I'm Gym Leader Block. Let's battle!")
        battle("Gym Leader Block", 40)
      
      #if player is at the starting location and moves south, they will go into the lab
      elif (tuple(m.getPlayerLocation()) in lab) and ("s" in x.lower()):
        if len(inventory) == 1:
          doctor1()
        else:
          doctor2()
      else:
        images()


def intro():
  #introduce the player to the game and their goal for it.
  text = "Welcome, trainer! My name is Dred. I am the Doctor's grandson and I will help you "
  text += "through your time here. Your task, should you choose to accept it "
  text += "is to take over the faux-kemon gym in Alloy City. The leader has "
  text += "decided it is time for her to move on to the next great "
  text += "adventure. She has invited several trainers to challenge her "
  text += "and prove their worth. If you wish to take over the gym then "
  text += "tell me your name so I may inform gym leader Block of your pending "
  text += "arrival."
  
  #we used text boxes throughout the game as it would give a better flow
  showInformation(text)
  
  #if we take in the player's name, they feel like it is more personalized even if we don't really care what their name is
  global name
  name  = requestString("What is your name?")
  if name == "":
    name = "Red Circle"
  
  txt = "Well, " + name + " south of you is the lab. Doctor Bloak will be waiting for you. "
  txt += "You may encounter more pokemon during your journey to the gym. The more creatures you "
  txt += "battle, the stronger you will become. Without further delay, carry on your journey. "
  showInformation(txt)

#These instructions should pop up when the player types help
def instructions():
  text = "To move, use the keys \'n, s, e, w\'. You may also use a multile of that by typing \'2n\', etc. "
  text += "You are able to hold 5 faux-kemon at a time and cannot trade them out. Battling "
  text += "other pokemon will make you stronger in order to take on the gym leader. You "
  text += "can see what pokemon you have at any time after visiting the doctor by typing \'inventory\'. "
  text += "You may also type \'help\' at any time to redisplay this information or \'exit\' to quit the game."
  

#starting information regarding the player's health, etc.
def initUser():
  global userHealth
  userHealth = 10
  global inventory
  inventory = ["Pakachu"]
  global fought
  #player's health will increase for each faux-kemon they have
  global userHealth
  userHealth = len(inventory) * 10
  #player's health will increase for each trainer they fought  
  #for x in fought:
    #userHealth += 3
  global enemyHealth
  enemyHealth = 0


#you will receive fauxkemon which will increase the user's overall health
def doctor1():
  text = "Welcome to Dr. Bloak's lab! Here he researches everything there is to know about faux-kemon. "
  text += "I have been working with my granddad for many years collecting faux-kemon for him to study. "
  text += "Enough of that though. You are here to get your faux-kemon! We have taken good care of it since "
  text += "you left it with us. Here you go!"
  global inventory
  inventory.extend(["Voldetort", "Red Baron", "Branch Manager"])
  show(getMedia("img", "starters"))
  text += "You better be off to the forest to meet up with Gym Leader Block. She will be waiting for you!"
  showInformation(text)


def doctor2():
  #if the user already has the fauxkemon, they don't need to be at the lab, so no new information is needed.
  text = "You best be getting along now " + name + " or you will miss Block. I hear she is on her way "
  text += "out of town. You will find her gym at the end of the Green Forest. There are many trainers "
  text += "looking to hone their skills in the forest. If you battle them, you will become stronger. "
  text += "The exit to the lab is just to the south. Good luck!"
  showInformation(text)


def battle(eName, eHealth):
  global userHealth
  global inventory
  global fought
  userHealth = len(inventory) * 10
  
  enemyName = eName
  enemyHealth = eHealth
  round = 0
  userDamageScale = (enemyHealth * .66)

  showInformation("Prepare to battle " + str(enemyName) + "!")

  # Battle until one combatant loses
  while ((userHealth > 0) and (enemyHealth > 0)):

    round += 1
    showInformation("Round " + str(round) + "!")

    # Player rolls for damage & hit/miss
    userDamage = random.randrange(1, int(userDamageScale))
    userHit = random.randrange(0,100)

    if (userHit > 12):
        showInformation("You strike the enemy for " + str(userDamage) + " damage!")

        enemyHealth -= userDamage
        
        text = "Turn Summary:\n"
        text += "Damage dealt: " + str(userDamage) + "\n"
        text += enemyName + " health: " + str(enemyHealth) + "\n"
        text += "Hero health: " + str(userHealth)
        showInformation(text)
        
    else:
        showInformation("Your blow falls short of hitting the enemy!")
        
        text = "Turn Summary:\n"
        text += "Damage dealt: 0\n"
        text += enemyName + " health: " + str(enemyHealth) + "\n"
        text += "Hero health: " + str(userHealth)
        showInformation(text)

    # Check to see if enemy is still alive after player turn has ended
    if (enemyHealth > 0):

        # Enemy rolls for damage & hit/miss
        enemyDamage = random.randrange(0,3)
        enemyHit = random.randrange(0,100)

        if (enemyHit > 13):
            showInformation("The enemy blow connects and deals " + str(enemyDamage) + " damage!")

            userHealth -= enemyDamage

            text = "Turn Summary:\n"
            text += "Damage taken: " + str(enemyDamage) + "\n"
            text += enemyName + " health: " + str(enemyHealth) + "\n"
            text += "Hero health: " + str(userHealth)
            showInformation(text)
        else:
            showInformation("The enemy swings and misses, leaving themselves exposed for a devastating counter attack!")
            text = "Turn Summary:\n"
            text += "Damage taken: 0\n"
            text += enemyName + " health: " + str(enemyHealth) + "\n"
            text += "Hero health: " + str(userHealth)
            showInformation(text)

  # Win
  if (enemyHealth <= 0):
    showInformation("Congratulations, you bested your foe and leave the battle victorious!")
    userHealth += 3

  # Lose
  if (userHealth <= 0):
    showInformation("Unable to best your challenger, you retire to your quarters draped in defeat.")
    sys.exit() 


def images():
  h = random.randint(0, 30)
  if h < 6:
    stopPlaying(viridian)
    if h == 0:
      play(battleSong)
      battlepic = getMedia("img", "vulpix")
      show(battlepic)
      showInformation("A wild Firecat has appeared!")
      battle("Firecat", 10)
      stopPlaying(battleSong)
      play(viridian)
    if h == 1:
      play(battleSong)
      battlepic = getMedia("img", "vaporeon")
      show(battlepic)
      showInformation( "A wild Waterdog has appeared!")
      battle("Waterdog", 10)
      stopPlaying(battleSong)
      play(viridian)
    if h == 2:
      play(battleSong)
      battlepic = getMedia("img", "snorlax")
      show(battlepic)
      showInformation( "A wild Snoreman has appeared!")
      battle("Snoreman", 10)
      stopPlaying(battleSong)
      play(viridian)
    if h == 3:
      play(battleSong)
      battlepic = getMedia("img", "mew")
      show(battlepic)
      showInformation( "A wild Psychat has appeared!")
      battle("Psychat", 10)
      stopPlaying(battleSong)
      play(viridian)
    if h == 4:
      play(battleSong)
      battlepic = getMedia("img", "jolteon")
      show(battlepic)
      showInformation( "A wild Shockydog has appeared!")
      battle("Shockydog", 10)
      stopPlaying(battleSong)
      play(viridian)
    if h == 5:
      play(battleSong)
      battlepic = getMedia("img", "squirtle")
      show(battlepic)
      showInformation( "A wild Voldetort has appeared!")
      battle("Voldetort", 10)
      stopPlaying(battleSong)
      play(viridian)


class Map():
  #Created 2017-04-16 by Kevin Hendershott.  My contribution to the team project.
  #Modified 2017-04-19 by Kevin Hendershott.  Changed all path from concatenated strings to os.path.join() functions per Lyndsay's suggestion to make code Mac-friendly.
  
  #Initializations:
  import os
  import re
  maps = []
  mapPic = None
  mapTopLeft = None
  sprites = []
  playerLocation = [0, 0]
  
  
  def __init__(self, mapFileName, devMode = False):
    self.mapFileName = mapFileName
    self.devMode = devMode
    self.dirThisModule = os.path.dirname(__file__)  #Determine path to this module to simplify other path declarations.
    
    if devMode:  #Comment out as necessary before a "dev" run, but must leave at least one statement "live" or the if statement will raise a syntax error at compile-time.
      #self.createMapSegments(mapFileName, 2, 3)
      #self.createMapAttributesLayer(mapFileName, writeSpriteFiles = True)  #Run twice, during development only: 1) creates unique sprites to be organized into passable/not; 2) creates final overlay file.
      self.createMapAttributesLayer(mapFileName, writeSpriteFiles = False)  #Run twice, during development only: 1) creates unique sprites to be organized into passable/not; 2) creates final overlay file.
    else:
      self.loadMaps()
      self.loadSpritesList(mapFileName)
      self.setPlayerStartingLoc(mapFileName)
      self.displayCurrentMap(initializing = True)
  
  
  def getPlayerLocation(self):
    return self.playerLocation
    
  
  def displayCurrentMap(self, initializing=False):
    mapFound = False
    for m in self.maps:
      if m[1] <= self.playerLocation[0] and self.playerLocation[0] <= m[3]:
        if m[2] <= self.playerLocation[1] and self.playerLocation[1] <= m[4]:
          if initializing:
            self.mapPic = makePicture(os.path.join(self.dirThisModule, "sprites", m[0]))
            self.mapTopLeft = m[1], m[2]
            show(self.mapPic)
          else:
            if self.mapTopLeft == (m[1], m[2]):
              #Map has not changed, so just repaint to show the replaced sprites.
              repaint(self.mapPic)  #Don't call repaint() by without first calling show() or it keeps opening new pictures.  (Not sure this line is actually doing anything.)
            else:
              copyInto(makePicture(os.path.join(self.dirThisModule, "sprites", m[0])), self.mapPic, 0, 0)
              self.mapTopLeft = m[1], m[2]
              show(self.mapPic)
          self.displayPlayer(m[1], m[2])
          mapFound = True
        else:
          pass  #Keep looking.  I realize this statement is not necessary, but I like it here for documentation that all logic paths were explored, so there.
      else:
        pass    #Keep looking.
    if not mapFound:
      showInformation("Error - cannot locate current map.")  #If you get this far, no map was found.
  
  
  def movePlayer(self, movement):
    #Assumes movement is a number (or not) in front of, and immediately adjacent to, a letter for a cardinal direction, i.e. "N", "9E", "12s", "w", etc.
    #We all agree that if user makes nonsensicle entry, or tries to move into barrier, or untimately just doesn't move, we do nothing - they should see that they didn't move.
    #Don't need to worry about edges of map since all the edges have adjacent barrier so that takes care of itself.
      newLocation = self.playerLocation[:]  #Be careful to set value, not reference here.
      tempList = self.re.split("(\d+)", movement)
      if "" in tempList:
        tempList.remove("")
      if len(tempList) == 1:
        tempList.append(tempList[0])  #Trick to copy "n" and make sure there's both a value at item[0] and item[1] until I can revisit the following logic and make it better.
      if tempList[0].isnumeric():
        qty = int(tempList[0])
      else:
        qty = 1
      if tempList[1].isalpha():
        direction = tempList[1][0].lower()  #Just want the first letter, and forced to lowercase.
        while qty > 0:
          if direction == "n":
            newLocation[1] -= 16
          elif direction == "s":
            newLocation[1] += 16
          elif direction == "e":
            newLocation[0] += 16
          elif direction == "w":
            newLocation[0] -= 16
          else:
            pass  #Nonsensical input.
          if str(newLocation) == str(self.playerLocation):  #Be careful to compare values here, not references.
            pass  #Player didn't move.
          else:
            if self.passable(newLocation[0], newLocation[1]):
              self.replaceSprite(self.playerLocation[0], self.playerLocation[1])
              self.playerLocation = newLocation[:]  #be careful to set value, not reference here.
              self.displayCurrentMap(initializing = False)
              #self.displayPlayer()  #Moved this to displayCurrentMap().
            else:
              return None  #Not passable, so stop moving (and exit function).
          qty -= 1
      else:
        pass  #Nonsensical input.
  
  
  def replaceSprite(self, x, y):
    for sprite in self.sprites:
      if sprite[1] == x and sprite[2] == y:  #Once correct sprite is located,
        if sprite[3]:
          folder = "passable"
        else:
          folder = "impassable"
        x1 = self.mapTopLeft[0]
        y1 = self.mapTopLeft[1]
        copyInto(makePicture(os.path.join(self.dirThisModule, "sprites", folder, sprite[0])), self.mapPic, x - x1, y - y1)
  
  
  def passable(self, x, y):
    for sprite in self.sprites:
      if sprite[1] == x and sprite[2] == y:  #Once correct sprite is located,
        return sprite[3]                     #Return either True of False.  Yes, I'm letting an implicit type conversion happen here, maybe, but it works.
  
  
  def displayPlayer(self, xTopLeft, yTopLeft):
    #addRectFilled(self.mapPic, self.playerLocation[0] - xTopLeft, self.playerLocation[1] - yTopLeft, 16, 16, red)
    addOvalFilled(self.mapPic, self.playerLocation[0] - xTopLeft, self.playerLocation[1] - yTopLeft, 16, 16, red)
  
  
  def setPlayerStartingLoc(self, mapFileName):
    if mapFileName == "Forest.png":
      self.playerLocation = [352+(13*16), 736+(16*16)]  #Starting position for Forest.
    else:
      self.playerLocation = [0, 0]
  
  
  def loadMaps(self):
    for fileName in os.listdir(os.path.join(self.dirThisModule, "sprites")):
      if fileName[len(fileName)-len(".jpg"):] == ".jpg":
        tempPic = makePicture(os.path.join(self.dirThisModule, "sprites", fileName))
        xTopLeft = int(fileName[len(fileName)-13:len(fileName)-9])
        yTopLeft = int(fileName[len(fileName)-8:len(fileName)-4])
        xBottomRight = xTopLeft + getWidth(tempPic) - 1
        yBottomRight = yTopLeft + getHeight(tempPic) - 1
        tuple = (fileName, xTopLeft, yTopLeft, xBottomRight, yBottomRight)
        self.maps.append(tuple)
  
  
  def strToBool(self, s):  #Attempt to make up for Python's horrible bool() function, e.g. bool('False') returns True!!!!  I hate Python because of shit like this.
    s = s.strip()  #Make sure to eliminate any leading or trailing whitespace before testing.  I neglected to do this originally and spent an hour chasing my tail.
    if s == "True" or s == "'True'" or s == "\"True\"":
      return True
    elif s == "False" or s == "'False'" or s == "\"False\"":
      return False
    else:
      return None  #I might change this to default to False someday.  I'll try this for now, but the expectation is that input is always exact string.  
  
  def loadSpritesList(self, mapFileName):
    fileName = mapFileName[:len(mapFileName)-len(".png")] + "_overlay.txt"  #My version of file.name since file.name contains the entire path, and I don't always want the entire path.
    filePath = os.path.join(self.dirThisModule, fileName)
    if os.path.exists(filePath):
      try:
        fileIn = open(filePath)
      except:
        print "Well that didn't work very well.  This file %s failed to open for reasons unknown:  " % (fileIn.name)
      for line in fileIn:              #Even though we stored these as tuples into a text file, the reverse does not preserve the "tuppleness", so...
        line = line.strip()            #Remove whitespace from ends which will eliminate newline characters.
        line = line[1:len(line)-1]     #Remove tuple-like parentheses from ends.
        tmp = line.strip().split(",")  #Split tuple-like string back into its original elements, once again stripping away the whitespace that may come after the commas.
        self.sprites.append((tmp[0].strip("'"), int(tmp[1]), int(tmp[2]), self.strToBool(tmp[3])))  #Store as tuple.  Have to strip quotes or they get doubled-up by append.
      try:
        fileIn.close()
      except:
        print "Well that didn't work very well.  This file %s failed to close for reasons unknown:  " % (fileIn.name)
  
  
  def createMapSegments(self, mapFileName, xDivisor, yDivisor):
    #Created 2017-04-15 by Kevin Hendershott.
    #Map passed in MUST HAVE even dimensions.  Odd dimensions are not handled herein (yet).
    #Divisors passed in MUST HAVE even results.  Odd results are not handlded herein (yet).
    #Only for use at development-time to help construct game, not for production use.  Saves us from having to hand-make map segments.

    mapPic = makePicture(os.path.join(self.dirThisModule, mapFileName))
    w = getWidth(mapPic)
    h = getHeight(mapPic)
    xSegment = w / xDivisor
    ySegment = h / yDivisor
    for x in range(0, w, xSegment):
      for y in range (0, h, ySegment):
        mapSegment = makeEmptyPicture(xSegment, ySegment, magenta)  #Magenta is a safety net to see if any pixels were missed. Magenta is easy to see, and will likely be our chromakey choice later.
        for x1 in range(0, xSegment):
          for y1 in range(0, ySegment):
            setColor(getPixelAt(mapSegment, x1, y1), getColor(getPixelAt(mapPic, x + x1, y + y1)))  #Grab a 16x16 piece of the bigger map.  We call this little image a sprite.
        fileName = "%s_%0*d_%0*d.jpg" % (mapFileName[:len(mapFileName)-len(".png")], 4, x, 4, y)              #create a useful, unique filename for it (whether ultimately used or not), and
        writePictureTo(mapSegment, os.path.join(self.dirThisModule, "sprites", fileName))           #write it out to a folder to be sorted later into "passable" and "impassible" areas.
  
  
  def createMapAttributesLayer(self, mapFileName, writeSpriteFiles = True):
    #Created 2017-04-15 by Kevin Hendershott.
    #Only for use at development-time to help construct game, not for production use.  Saves us from having to hand-make a passability overlay.
    #Run twice, during development only: 1) creates unique sprites to be organized into passable / impassable; 2) creates final overlay file based on passable / impassable decisions from the first run.
    #Parses the map into 16x16 sprites and saves off the unique ones so the programmers can select which will be passible (grass & sand) and impassible (trees and walls), etc.
    #Also parses the map into even large segements.  In the case of Forest.png, it will be 22 sprites wide by 23 sprites high.  Hard-coded for now, programmatically another day.
    #Assumes map is divisible by 16 in both directions, and animation movements will also be 16x16.
    #Can later be made to add other attributes such as "type" (sand, grass, cabbage, steps, tree, wall, sign, flowers, etc.) and any other map attribute deemed necessary.
    
    sprites = []
    uniqueSprites = []
    passabilityList = []
    for p in ("impassable", "passable"):
      for fn in os.listdir(os.path.join(self.dirThisModule, "sprites", p)):
        #tuple = (makePicture(os.path.join(self.dirThisModule, "sprites", p, fn), fn, p)  #Abandoned trying to match the pictures themselves.  Apparently when recreated this way, the pic is incomparable to one created looping through pixels, below.
        tuple = (fn, p)
        passabilityList.append(tuple)
    mapPic = makePicture(os.path.join(self.dirThisModule, mapFileName))
    w = getWidth(mapPic)
    h = getHeight(mapPic)
    for x in range(0, w, 16):
      for y in range(0, h, 16):
        sprite = makeEmptyPicture(16, 16, magenta)  #Magenta is a safety net to see if any pixels were missed. Magenta is easy to see, and will likely be our chromakey choice later.
        for x1 in range(0, 16):
          for y1 in range(0, 16):
            setColor(getPixelAt(sprite, x1, y1), getColor(getPixelAt(mapPic, x + x1, y + y1)))  #Grab a 16x16 piece of the bigger map.  We call this little image a sprite.
        fileName = "sprite_%0*d_%0*d.jpg" % (4, x, 4, y)                                        #create a useful, unique filename for it (whether ultimately used or not), and
        if str(getPixels(sprite)) not in (str(getPixels(s[0])) for s in uniqueSprites):         #If it is not already in the list of s#prites,
          uniqueSprites.append((sprite, fileName, x, y))                                        #append the sprite to the list of unique sprits, and
          if writeSpriteFiles:
            writePictureTo(sprite, os.path.join(self.dirThisModule, "sprites", fileName))       #write it out to a folder to be sorted later into "passable" and "impassible" areas.
          resemblesFileName = fileName
        else:
          for t in uniqueSprites:
            if str(getPixels(sprite)) == str(getPixels(t[0])):
              resemblesFileName = t[1]
        for p in passabilityList:
          if p[0] == resemblesFileName:
            if p[1] == "passable":
              passable = True
            elif p[1] == "impassable":
              passable = False
            else:  #Default choice for passable:
              passable = True
        sprites.append((resemblesFileName, x, y, passable))
    file = open(os.path.join(self.dirThisModule, mapFileName[:len(mapFileName)-len(".png")] + "_overlay.txt"), "w")
    for s in sprites:
      file.write("%s\n" % str(s))
    file.close()
    

#user can exit game at any time
def leave():
  showInformation("I see you have decided to seek adventure elsewhere. Good luck on your journey!")
  sys.exit()