import random
import numpy

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