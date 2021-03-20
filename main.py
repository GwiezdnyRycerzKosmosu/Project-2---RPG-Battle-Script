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
enemy_spells = [fire, meteor, cure]


# Instantiate People
player1 = Person("Kulfon ",3260, 165, 360, 34, player_spells, player_items)
player2 = Person("Kajko  ",4160, 165, 360, 34, player_spells, player_items)
player3 = Person("Kokosz ",3089, 165, 360, 34, player_spells, player_items)
players = [player1, player2, player3]

enemy1 = Person("Imp    ", 1200, 165, 545, 325, enemy_spells, [])
enemy2 = Person("Villain", 12000, 565, 545, 25, enemy_spells, [])
enemy3 = Person("Troll  ", 1200, 165, 545, 325, enemy_spells, [])
enemies = [enemy1, enemy2, enemy3]


# Counter of defeated
defeated_enemies = 0
defeated_players = 0


running = True
i=0
print(bcolors.FAIL +bcolors.BOLD+"AN ENEMY ATTACKS!"+bcolors.ENDC)
while running:
    print("==============================================================")
    print("PLAYERS:                   HP                                    MP")
    for player in players:
        player.get_stats()
    print("\n")
    print("ENEMIES:                   HP")
    for enemy in enemies:
        enemy.get_enemy_stats()



    # Player phase

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice)-1

        # Choose attack
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.OKBLUE+"\nYou attacked for", dmg, "points of damage to " + enemies[enemy].name + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
                defeated_enemies += 1
        # Choose magic
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
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE +"\n" +spell.name + " deals", str(magic_dmg), "points of damage to " +
                      enemies[enemy].name + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
                defeated_enemies += 1
        # Choose item
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
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" +item.name + " deals", str(item.prop), "points of damage for" +
                      enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
                    defeated_enemies += 1


    # Check if battle is over

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        runnig = False


    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        target = random.randrange(0, 2)

        # Choose attack
        if enemy_choice == 0:
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + " " + enemy.name.replace(" ", "") +" attacks for", str(enemy_dmg) + " points of damage to "
                  + players[target].name + bcolors.ENDC )
            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died.")
                del players[target]
                defeated_players += 1

        # Choose magic
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()

            print(bcolors.FAIL + enemy.name.replace(" ", "") +" chose", spell.name + bcolors.ENDC)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.FAIL + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      players[target].name + bcolors.ENDC)
            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died.")
                del players[target]
                defeated_players += 1




