import random
import math

from slayers.Equipment import Equipment

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
      align = "^"
      width = 15

      if stat.lower() in ["name", "money"]:
        print("\n{:8}:{:}\t\t{:8}:{:}\n".format(args[i],displayStats[offset], args[i],displayStats[offset+1]))

      elif self.isBarStat(stat):
        print("{:8}:{:4}/{:4}\t\t{:8}:{:4}/{:4}".format(args[i],displayStats[offset][0],displayStats[offset][1], args[i],displayStats[offset+1][0], displayStats[offset+1][1]))

      else:
        print("{:8}:{:4} {:+.0f}\t\t{:8}:{:4} {:+.0f}".format(args[i],displayStats[offset][1],self.statsFromEquipment(args[i]), args[i],displayStats[offset+1][1], Combatant.statsFromEquipment(args[i])))

      offset += 2
    
    for slot in self.equipment:
      print("{:8}:{:15}\t\t{:8}:{:15}".format(slot, self.equipment[slot].name if self.equipment[slot] else "None", slot, Combatant.equipment[slot].name if Combatant.equipment[slot] else "None"))

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

