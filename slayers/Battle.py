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
      print(combatant.name + " attacked " + opponent.name + " for {:d} point of damage.".format(int(damage)))
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