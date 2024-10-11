from straw_hat import *
from heap import *
from treasure import *






treasury = StrawHatTreasury(3)
treasury.add_treasure(Treasure(1, 8, 1))
treasury.add_treasure(Treasure(2, 7, 2))
treasury.add_treasure(Treasure(3, 4, 4))
treasury.add_treasure(Treasure(4, 1, 5))
print(treasury.get_completion_time())
