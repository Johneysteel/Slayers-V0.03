import random, math

class Equipment(object):
  def __init__(self, name = "unidentified", slot="none"):
    self.name = name
    self.stats = {"strength":0,
                  "defence": 0,
                  "speed":0
                  }
    self.slot = slot

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
      if fighter.speed[0] > highestspeed:
        highestspeed = fighter.speed[0]
    return highestspeed
  
class Combatant(object):

  def __init__(self):
    self.name = self.randomName()
    self.pool = 20

    self.strength = [1,1]
    self.speed = [1,1]
    self.defence = [1,1]
    self.health = [10,10]

    self.money = random.randint(0,65)

    self.randomSkills(self.pool)
    self.resetStats()

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
    return random.randint(0, self.strength[0])
  
  def calculateAbsorb(self, damage, opponent):
    if damage >= opponent.defence[0]:
      return damage - opponent.defence[0]
    else:
      percent = damage/opponent.defence[0]
      return math.floor(percent * damage)

  def canAttack(self):
    return self.nextAttack >= 1

  def updateAttackRate(self, highestSpeed):
    self.attackRate = self.speed[0]/highestSpeed

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
    print("Strength Level: " + str(self.strength[1]))
    print("Speed Level: " + str(self.speed[1]))
    print("Defence Level: " + str(self.defence[1]))
    print("\nHealth:" + str(self.health[0]) + " / " + str(self.health[1]))

    print("\nMoney: " + str(self.money) + " gold.")

  def equip(self, Equipment):
    for slot in self.equipment:
      if Equipment.slot.lower() == slot.lower():
        self.equipment[slot] = Equipment
        break
    
# Create fighters
fighter1 = Combatant()
fighter2 = Combatant()

# Display fighters stats
fighter1.examine()
fighter2.examine()

#battle = Battle()

#battle.Fight(fighter1,fighter2)

iron_helmet = Equipment("Iron Helmet","head")
leather_chaps = Equipment("Leather Chaps","Legs")

fighter1.equip(iron_helmet)
fighter1.equip(leather_chaps)

for slot in fighter1.equipment:
  if fighter1.equipment[slot]:
    print(slot + " | " + fighter1.equipment[slot].name + " | " + str(fighter1.equipment[slot].stats))
  else:
    print(slot + " | " + "None")