import random, math, numpy

class Equipment(object):
  stats = ["strength", "defence", "speed"]
  wood = ["Oak", "Burch", "Pine"]
  metal = ["bronze", "iron", "steel"]
  hide = ["leather", "snake hide", "alligator hide"]
  weapon = ["short sword", "long sword", "battle axe", "hammer", "dagger"]
  sheild = ["round shield", "square shield"]
  jewelry = ["opal", "silver", "gold", "sapphire", "emerald", "ruby", "diamond"]
  material = metal + hide
  
  def __init__(self, name = "unidentified", slot=None, stats={}):
    self.name = name
    self.stats = stats
    self.slot = slot

    if not self.stats:
      numberOfSkills = (random.choice([2,3]))
      stats = random.sample(Equipment.stats, numberOfSkills)
      print("Randomly choosen stats: {}".format(stats))
      for stat in stats:
        self.stats[stat] = 0
  

  def generateStatsByRate(self, points, negative_rate=None):
    if not negative_rate:
      # Random Percent of negative points 10-30%
      self.negative_rate = random.choice([.3,.2,.1])
    
    self.positive_rate = 1-self.negative_rate

    # Generate a set of random values based on number of stats
    randomPositiveValues = numpy.random.random(len(self.stats))
    randomNegativeValues = numpy.random.random(len(self.stats))
    
    # Divide each value by the sum of all the values to get the average
    randomPositiveValues /= sum(randomPositiveValues)
    randomNegativeValues /= sum(randomNegativeValues)

    # Scale and round the actual Values
    self.positivePoints = [round(x * points * self.positive_rate) for x in randomPositiveValues]
    self.negativePoints = [round(x * points * self.negative_rate) for x in randomNegativeValues]


    generatedStats = [positive - negative for positive, negative in zip(self.positivePoints,self.negativePoints)]

    i = 0
    for stat in self.stats:
      self.stats[stat] = generatedStats[i]
      i += 1

  def displayValues(self):
    total = sum(self.positivePoints) + sum(self.negativePoints)
    
    print("\nPositive_Rate: {}\nNegative Rate: {}\nPositive Points:{}\nNegative Points: {}".format(self.positive_rate, self.negative_rate, self.positivePoints, self.negativePoints))
    print("{} stats: {}".format(self.name, self.stats))

    print("\nSum Positive:{}\nSum Negative:{}\nDifference:{}\nTotal:{}".format(sum(self.positivePoints), sum(self.negativePoints), sum(self.positivePoints) - sum(self.negativePoints), total))
  
  def generateStatsByLevel(self, level, negative_rate = None):
    points = level * 20
    self.generateStatsByRate(points, negative_rate)

  def randomEquipment(self, level, slot=None):
    if not slot:
      slot = self.slot

    if self.slot.lower() == "head":
      self.name = "{} helmet".format(random.choice(Equipment.material))

    elif self.slot.lower() == "neck":
      self.name = "{} amulet".format(random.choice(Equipment.jewelry))
      
    elif self.slot.lower() == "body":
      self.name = "{} body armour".format(random.choice(Equipment.material))
      
    elif self.slot.lower() == "legs":
      self.name = "{} leg armour".format(random.choice(Equipment.material))
      
    elif self.slot.lower() == "feet":
      self.name = "{} boots".format(random.choice(Equipment.material))
      
    elif self.slot.lower() == "mainhand":
      self.name = "{} {}".format(random.choice(Equipment.metal), random.choice(Equipment.weapon))
    
    elif self.slot.lower() == "offhand":
      self.name = "{} {}".format(random.choice(Equipment.wood + Equipment.metal), random.choice(Equipment.sheild))

    self.generateStatsByLevel(level)

#V0.03 - Equipment   
class Battle(object):
  # 1v1 Combat - Turns based on speed
  def Fight(self, fighter1, fighter2):
    
    while fighter1.isAlive() and fighter2.isAlive():
      highestSpeed = self.getHighestSpeed([fighter1, fighter2])

      fighter1.updateAttackRate(highestSpeed)
      fighter2.updateAttackRate(highestSpeed)
 
      fighter1.nextAttack += fighter1.attackRate
      fighter2.nextAttack += fighter2.attackRate

      if fighter1.canAttack():
        self.displayAttack(fighter1, fighter2)
        self.checkDead(fighter2)

      if fighter2.canAttack():
        self.displayAttack(fighter2, fighter1)
        self.checkDead(fighter1)

  def displayAttack(self, combatant, opponent):
    # If combatant is no longer alive
    if not combatant.isAlive():
      return # prevent attack

    # Damage will be -2 for block, -1 for miss, 0 or a positive int
    damage = combatant.attack(opponent)
    
    if damage == -2:
      print(combatant.name + " attacked " + opponent.name + " but was blocked!")
    elif damage == -1:
      print(combatant.name + " attacked " + opponent.name + " but missed!")
    elif damage > 0:
      print(combatant.name + " attacked " + opponent.name + " for " + str(damage) + " point of damage.")
    else:
      print(combatant.name + " attacked " + opponent.name + " but did no damage.")
  
  def checkDead(self, fighter):
    if not fighter.isAlive():
      print (fighter.name + " has been defeated.")

  def getHighestSpeed(self, fighters):
    highestspeed = 0
    
    for fighter in fighters:
      # Gets the fighter's speed stat plus speed from equipment
      totalSpeed = fighter.speed[0] + fighter.statsFromEquipment("speed")
      
      if totalSpeed > highestspeed:
        highestspeed = totalSpeed

    return highestspeed
  

class Combatant(object):

  def __init__(self):
    self.name = self.randomName()
    self.pool = 200
    self.level = 1

    self.strength = [1,1]
    self.speed = [1,1]
    self.defence = [1,1]
    self.health = [10,10]
    
    self.money = random.randint(0,65)

    self.randomSkills(self.pool)

    # Combat variables
    self.attackRate = 0
    self.nextAttack = 0

    # Equipment
    self.equipment = {
                      "head":None,
                      "neck":None,
                      "mainhand":None,
                      "offhand":None,
                      "body":None,
                      "legs":None,
                      "feet":None
                      }

  def attack(self, Combatant):

    # Reset NextAttack variable
    self.nextAttack -= 1

    # Calculate Random Damage
    damage = self.calculateDamage()

    # -1 indicates missed attack
    if damage == 0:
      return -1

    # Calculate Absorbed Damage
    damage = self.calculateAbsorb(damage, Combatant)

    # -2 indicates blocked attacked
    if damage == 0:
      return -2
    
    # Subtract damage from opponent's current health    
    Combatant.health[0] -= damage
    
    return damage

  def calculateDamage(self):
    return random.randint(0, self.strength[0] + self.statsFromEquipment("strength"))
  
  # Calculate's Damage based on incoming damage and opponent object
  def calculateAbsorb(self, damage, opponent):

    # Calculate opponent's defence from stats + equipment
    opponentDefence = opponent.defence[0] + + self.statsFromEquipment("defence")

    if damage >= opponentDefence:
      return damage - opponentDefence
    else:
      percent = damage/opponentDefence
      return math.floor(percent * damage)

  def canAttack(self):
    return self.nextAttack >= 1

  def updateAttackRate(self, highestSpeed):
    self.attackRate = (self.speed[0] + self.statsFromEquipment("speed"))/highestSpeed

  def isAlive(self):
    return self.health[0] >= 1 

  def randomSkills(self, pool):
    a = random.randint(0,pool)
    pool -= a
    b = random.randint(0,pool)
    pool -= b
    c = random.randint(0,pool)
    pool -= c
    d = pool
    pool -= d

    self.strength[1] += a
    self.speed[1] += b
    self.defence[1] += c
    self.health[1] += d * 10

    self.resetStats()

  def resetStats(self):
    self.strength[0] = self.strength[1]
    self.speed[0] = self.speed[1]
    self.defence[0] = self.defence[1]
    self.health[0] = self.health[1]

  def randomName(self):
    return random.choice(["Skeleton", "Troll", "Goblin", "Undead"])

  def examine(self):
    print(self.name)
    print(len(self.name) * "-")
    print("Strength Level:{}".format(self.strength[1]))
    print("Speed Level:{}".format(self.speed[1]))
    print("Defence Level:{}".format(self.defence[1]))
    print("\nHealth:{}/{}".format(self.health[0], self.health[1]))

    print("\nMoney:{} gold\n".format(self.money))

  def equip(self, Equipment):
    for slot in self.equipment:
      if Equipment.slot.lower() == slot.lower():
        self.equipment[slot] = Equipment
        break

  def compare(self, Combatant, *args):
    if not args:
      args = ["name", "health","strength", "speed", "defence","money"]
    
    displayStats = []

    for attribute in args:
      if attribute in dir(self) and attribute in dir(Combatant):
        displayStats.append(self.__getattribute__(attribute))
        displayStats.append(Combatant.__getattribute__(attribute))

    offset = 0
    for i in range(len(args)):
      stat = args[i]

      if stat.lower() in ["name", "money"]:
        print("\n{}:{}\t\t{}:{}\n".format(args[i],displayStats[offset], args[i],displayStats[offset+1]))

      elif self.isBarStat(stat):
        print("{}:{}/{}\t\t{}:{}/{}".format(args[i],displayStats[offset][0],displayStats[offset][1], args[i],displayStats[offset+1][0], displayStats[offset+1][1]))

      else:
        print("{}:{} {}\t\t{}:{} {}".format(args[i],displayStats[offset][1],self.statsFromEquipment(args[i]), args[i],displayStats[offset+1][1], Combatant.statsFromEquipment(args[i])))

      offset += 2
    
    for slot in self.equipment:
      print("{}:{}\t\t{}:{}".format(slot, self.equipment[slot].name if self.equipment[slot] else None, slot, Combatant.equipment[slot].name if Combatant.equipment[slot] else None))

  def isBarStat(self, stat):
    return stat in ["health", "mana"]
  
  def generateRandomEquipment(self, amount):
    maximumEquipment = len(self.equipment)

    if 0 > amount:
      amount = 0
    
    if amount < maximumEquipment:
      amount = maximumEquipment
    
    slots = random.sample(self.equipment.keys(),random.randrange(0,amount+1))
    for slot in slots:
      equipment = Equipment(slot=slot, stats={})
      equipment.randomEquipment(3)
      self.equip(equipment)
  
  def statsFromEquipment(self, stat):
    slotsWithEquipment = [self.equipment[slot] for slot in self.equipment if self.equipment[slot]]

    return sum([item.stats[stat] for item in slotsWithEquipment if stat in item.stats])


print("====== Program Start ======")    
# Create fighters
fighter1 = Combatant()
fighter2 = Combatant()

#Equipt Armours
fighter1.generateRandomEquipment(3)
fighter2.generateRandomEquipment(3)

# Display fighters stats
fighter1.compare(fighter2)

battle = Battle()

battle.Fight(fighter1,fighter2)

print("====== Program End ======")