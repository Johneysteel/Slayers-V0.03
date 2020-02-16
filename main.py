from slayers.Combatant import Combatant
from slayers.Battle import Battle

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

#battle.Fight(fighter1,fighter2)

print("====== Program End ======")