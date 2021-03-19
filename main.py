from classes.game import Person, bcolors
from classes.Magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40 , 1200, "black")
quake = Spell("Quake", 14, 1500, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 35, 1500, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 250 HP", 250)
hipotion = Item("Hi-Potion", "potion", "Heals 500 HP", 500)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/MP of entire party", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor,quake, cure, cura]
player_items = [{"item":potion, "quantity":15}, {"item":hipotion, "quantity":5},
                {"item":superpotion, "quantity":5}, {"item":elixer, "quantity":5},
                {"item":hielixer, "quantity":2}, {"item":grenade, "quantity":5}]

# Instantiate People
player1 = Person("Kulfon :",3260, 165, 360, 34, player_spells, player_items)
player2 = Person("Kajko  :",4160, 165, 360, 34, player_spells, player_items)
player3 = Person("Kokosz :",3089, 165, 360, 34, player_spells, player_items)
players = [player1, player2, player3]
enemy = Person("Villain:", 12000, 565, 545, 25, [], [])

running = True
i=0
print(bcolors.FAIL +bcolors.BOLD+"AN ENEMY ATTACKS!"+bcolors.ENDC)
while running:
    print("==============================================================")
    print("NAME                     HP                                    MP")
    for player in players:
        player.get_stats()
    enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice)-1
        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print(bcolors.OKBLUE+"\n You attacked for", dmg, "points of damage."+bcolors.ENDC)
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" +spell.name + "heals for", str(magic_dmg), "HP."+ bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE +"\n" +spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left ... " + bcolors.ENDC)
                continue

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP", bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxhp
                    print(bcolors.OKGREEN + "\n" + item.name + "fully restored MP/HP of entire party" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" +item.name + "fully restored MP/HP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" +item.name + " deals", str(item.prop), "points of damege" + bcolors.ENDC)


    target = random.randrange(0,2)
    enemy_dmg = enemy.generate_damage()
    players[target].take_damage(enemy_dmg)
    print("\n" + bcolors.BOLD + bcolors.FAIL + "Enemy attacks " + players[target].name + " for", str(enemy_dmg) + " points of damage." + bcolors.ENDC +"\n")


    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player1.get_hp() == 0 or player2.get_hp() == 0 or player3.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        runnig = False



