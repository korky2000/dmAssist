#!/usr/bin/env python3

import json

class Character:
    def __init__(self, name, race, char_class, level, sub_class, ability_modifiers, proficiencies, actions, god, proficiency_bonus, saving_throws):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.sub_class = sub_class
        self.ability_modifiers = ability_modifiers
        self.proficiencies = [proficiency.lower() for proficiency in proficiencies]
        self.actions = actions
        self.god = god
        self.proficiency_bonus = proficiency_bonus
        self.saving_throws = [saving_throw.lower() for saving_throw in saving_throws]

    def get_stat(self, stat):
        skill_to_ability = {
            "athletics": "strength",
            "acrobatics": "dexterity",
            "sleight of hand": "dexterity",
            "stealth": "dexterity",
            "arcana": "intelligence",
            "history": "intelligence",
            "investigation": "intelligence",
            "nature": "intelligence",
            "religion": "intelligence",
            "animal handling": "wisdom",
            "insight": "wisdom",
            "medicine": "wisdom",
            "perception": "wisdom",
            "survival": "wisdom",
            "deception": "charisma",
            "intimidation": "charisma",
            "performance": "charisma",
            "persuasion": "charisma",
            "social interaction": "charisma"
        }

        stat = stat.lower()

        if stat in self.ability_modifiers:
            total_modifier = self.ability_modifiers[stat]
            if stat in self.saving_throws:
                total_modifier += self.proficiency_bonus
            return total_modifier

        ability = skill_to_ability.get(stat, None)
        if not ability:
            return None

        ability_modifier = self.ability_modifiers.get(ability, 0)
        total_modifier = ability_modifier

        if stat in self.proficiencies:
            total_modifier += self.proficiency_bonus

        return total_modifier

    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "char_class": self.char_class,
            "level": self.level,
            "sub_class": self.sub_class,
            "ability_modifiers": self.ability_modifiers,
            "proficiencies": self.proficiencies,
            "actions": self.actions,
            "god": self.god,
            "proficiency_bonus": self.proficiency_bonus,
            "saving_throws": self.saving_throws
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["race"],
            data["char_class"],
            data["level"],
            data["sub_class"],
            data["ability_modifiers"],
            data["proficiencies"],
            data["actions"],
            data["god"],
            data["proficiency_bonus"],
            data.get("saving_throws", [])
        )

    def display_info(self):
        info = f"""
------------------------
Name: {self.name}
Race: {self.race}
Class: {self.char_class}
Level: {self.level}
Subclass: {self.sub_class}
Ability Modifiers:
  Strength: {self.ability_modifiers.get("strength", 0)}
  Dexterity: {self.ability_modifiers.get("dexterity", 0)}
  Constitution: {self.ability_modifiers.get("constitution", 0)}
  Intelligence: {self.ability_modifiers.get("intelligence", 0)}
  Wisdom: {self.ability_modifiers.get("wisdom", 0)}
  Charisma: {self.ability_modifiers.get("charisma", 0)}
Proficiencies: {', '.join(self.proficiencies)}
Saving Throws: {', '.join(self.saving_throws)}
Actions:
  Bonus Actions: {self.actions['bonus_actions']}
  Extra Attacks: {self.actions['extra_attacks']}
  Actions: {self.actions['actions']}
God: {self.god}
Proficiency Bonus: {self.proficiency_bonus}
------------------------
        """
        return info.strip()

class God:
    def __init__(self, name, patronage, symbols, notable_followers, notes):
        self.name = name
        self.patronage = patronage
        self.symbols = symbols
        self.notable_followers = notable_followers
        self.notes = notes

    def to_dict(self):
        return {
            "name": self.name,
            "patronage": self.patronage,
            "symbols": self.symbols,
            "notable_followers": list(self.notable_followers),
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["patronage"],
            data["symbols"],
            set(data["notable_followers"]),
            data["notes"]
        )

    def display_info(self):
        info = f"""
------------------------
Name: {self.name}
Patronage: {', '.join(self.patronage)}
Symbols: {self.symbols}
Notable Followers: {', '.join(self.notable_followers)}
Notes: {self.notes}
------------------------
        """
        return info.strip()

class Shop:
    def __init__(self, name, town, type, shopkeep, inventory):
        self.name = name
        self.town = town
        self.type = type
        self.shopkeep = shopkeep
        self.inventory = inventory

    def to_dict(self):
        return {
            "name": self.name,
            "town": self.town,
            "type": self.type,
            "shopkeep": self.shopkeep,
            "inventory": self.inventory
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["town"],
            data["type"],
            data["shopkeep"],
            data["inventory"]
        )

    def display_info(self):
        inventory_list = "\n".join([f"  {item}: {price}" for item, price in self.inventory.items()])
        info = f"""
------------------------
Name: {self.name}
Town: {self.town}
Type: {self.type}
Shopkeep: {self.shopkeep}
Inventory:
{inventory_list}
------------------------
        """
        return info.strip()

class Town:
    def __init__(self, name, mayor, important_guilds, patron_gods):
        self.name = name
        self.mayor = mayor
        self.important_guilds = important_guilds
        self.patron_gods = patron_gods

    def to_dict(self):
        return {
            "name": self.name,
            "mayor": self.mayor,
            "important_guilds": self.important_guilds,
            "patron_gods": self.patron_gods
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["mayor"],
            data["important_guilds"],
            data["patron_gods"]
        )

    def display_info(self):
        info = f"""
------------------------
Name: {self.name}
Mayor: {self.mayor}
Important Guilds: {', '.join(self.important_guilds)}
Patron Gods: {', '.join(self.patron_gods)}
------------------------
        """
        return info.strip()

class Shopkeep:
    def __init__(self, name, town, shop, relationships, notes):
        self.name = name
        self.town = town
        self.shop = shop
        self.relationships = relationships
        self.notes = notes

    def to_dict(self):
        return {
            "name": self.name,
            "town": self.town,
            "shop": self.shop,
            "relationships": self.relationships,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["town"],
            data["shop"],
            data["relationships"],
            data["notes"]
        )

    def display_info(self):
        info = f"""
------------------------
Name: {self.name}
Town: {self.town}
Shop: {self.shop}
Relationships: {', '.join(self.relationships)}
Notes: {self.notes}
------------------------
        """
        return info.strip()

class Tavern:
    def __init__(self, name, town, barkeep, menu, accommodation, wealth, local_or_adventure, lodging, patrons, guild_associations):
        self.name = name
        self.town = town
        self.barkeep = barkeep
        self.menu = menu
        self.accommodation = accommodation
        self.wealth = wealth
        self.local_or_adventure = local_or_adventure
        self.lodging = lodging
        self.patrons = patrons
        self.guild_associations = guild_associations

    def to_dict(self):
        return {
            "name": self.name,
            "town": self.town,
            "barkeep": self.barkeep,
            "menu": self.menu,
            "accommodation": self.accommodation,
            "wealth": self.wealth,
            "local_or_adventure": self.local_or_adventure,
            "lodging": self.lodging,
            "patrons": self.patrons,
            "guild_associations": self.guild_associations
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["town"],
            data["barkeep"],
            data["menu"],
            data["accommodation"],
            data["wealth"],
            data["local_or_adventure"],
            data["lodging"],
            data["patrons"],
            data["guild_associations"]
        )

    def display_info(self):
        menu_list = "\n".join([f"  {item}: {price}" for item, price in self.menu.items()])
        accommodation_list = "\n".join([f"  {type}: {price}" for type, price in self.accommodation.items()])
        info = f"""
------------------------
Name: {self.name}
Town: {self.town}
Barkeep: {self.barkeep}
Menu:
{menu_list}
Accommodation:
{accommodation_list}
Wealth: {self.wealth}
Type: {self.local_or_adventure}
Lodging: {self.lodging}
Patrons: {', '.join(self.patrons)}
Guild Associations: {', '.join(self.guild_associations)}
------------------------
        """
        return info.strip()

def save_to_file(objects, filename):
    with open(filename, "w") as file:
        json.dump([obj.to_dict() for obj in objects], file)

def load_from_file(filename, cls):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [cls.from_dict(item) for item in data]
    except FileNotFoundError:
        return []

# Load existing data
characters = load_from_file("characters.json", Character)
gods = load_from_file("gods.json", God)
shops = load_from_file("shops.json", Shop)
towns = load_from_file("towns.json", Town)
shopkeeps = load_from_file("shopkeeps.json", Shopkeep)
taverns = load_from_file("taverns.json", Tavern)

def handle_add_tavern_command():
    try:
        name = input("Enter the name: ")
        town = input("Enter the town where the tavern is located: ")
        barkeep = input("Enter the name of the barkeep: ")
        menu = {}
        while True:
            item = input("Enter menu item name (or 'done' to finish): ")
            if item.lower() == 'done':
                break
            price = float(input(f"Enter price for {item}: "))
            menu[item] = price
        accommodation = {}
        while True:
            type = input("Enter accommodation type (or 'done' to finish): ")
            if type.lower() == 'done':
                break
            price = float(input(f"Enter price for {type}: "))
            accommodation[type] = price
        wealth = input("Enter the wealth level (poor, average, rich): ")
        local_or_adventure = input("Is it a local or adventure tavern?: ")
        lodging = input("Enter the type of lodging available: ")
        patrons = input("Enter patrons (comma separated): ").split(", ")
        guild_associations = input("Enter guild associations (comma separated): ").split(", ")

        new_tavern = Tavern(name, town, barkeep, menu, accommodation, wealth, local_or_adventure, lodging, patrons, guild_associations)
        taverns.append(new_tavern)
        save_to_file(taverns, "taverns.json")
        print(f"Tavern in {town} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_town_taverns_command(parts):
    town_name = " ".join(parts[:-1])
    town_taverns = [tavern for tavern in taverns if tavern.town.lower() == town_name.lower()]
    if town_taverns:
        for tavern in town_taverns:
            print(tavern.display_info())
    else:
        print(f"No taverns found in {town_name}.")

def handle_town_wealth_taverns_command(parts):
    town_name = parts[0]
    wealth_level = parts[1]
    town_wealth_taverns = [tavern for tavern in taverns if tavern.town.lower() == town_name.lower() and tavern.wealth.lower() == wealth_level.lower()]
    if town_wealth_taverns:
        for tavern in town_wealth_taverns:
            print(tavern.display_info())
    else:
        print(f"No {wealth_level} taverns found in {town_name}.")

def display_help():
    help_text = """
Available commands:
  help                      Show this help message
  add character             Add a new character
  add god                   Add a new god
  add shop                  Add a new shop
  add town                  Add a new town
  add shopkeep              Add a new shopkeep
  add tavern                Add a new tavern
  all shops                 List all shops
  all worships              List all worships
  bruh                      Print "bruh"
  check <stat> <name>       Check a character's stat
  <town> shops              List all shops in a town
  <town> taverns            List all taverns in a town
  <town> <wealth> taverns   List all taverns in a town with a specific wealth level
  <worship> followers       List all followers of a worship
  <character> info          Display character info
  <god> info                Display god info
  <god> search              Search for a god by name
  <god> of <patronage>      Search for a god by patronage
  edit god                  Edit god details
  edit character            Edit character details
  quit                      Exit the program
"""
    print(help_text)

def handle_check_command(parts):
    stat, name = parts[1], " ".join(parts[2:])
    character = next((char for char in characters if char.name.lower() == name.lower()), None)
    if character:
        stat_value = character.get_stat(stat)
        if stat_value is not None:
            print(f"{name}'s {stat} is {stat_value}")
        else:
            print(f"{name} does not have a stat or skill named {stat}")
    else:
        print(f"No character named {name} found.")

def handle_st_command(parts):
    town_name = " ".join(parts[:-1])
    print(f"Handling shops/taverns in town: {town_name}")

def list_all_worships():
    worships = set()
    for god in gods:
        worships.add(god.name)
    return "\n".join(sorted(worships))

def handle_worship_command(parts):
    worship = " ".join(parts[:-1])
    followers = [char.name for char in characters if char.god.lower() == worship.lower()]
    if followers:
        print(f"Followers of {worship}: {', '.join(followers)}")
    else:
        print(f"No followers of {worship} found.")

def handle_god_search_command(parts):
    search_name = " ".join(parts[2:])
    found_gods = [god for god in gods if search_name.lower() in god.name.lower()]
    if found_gods:
        for god in found_gods:
            print(god.display_info())
    else:
        print(f"No gods found matching the name {search_name}.")

def handle_god_of_command(parts):
    patronage = " ".join(parts[2:])
    found_gods = [god for god in gods if patronage.lower() in [p.lower() for p in god.patronage]]
    if found_gods:
        for god in found_gods:
            print(god.display_info())
    else:
        print(f"No gods found with patronage of {patronage}.")

def handle_followers_command(parts):
    god_name = " ".join(parts[:-1])
    followers = [char.name for char in characters if char.god.lower() == god_name.lower()]
    if followers:
        print(f"Followers of {god_name}: {', '.join(followers)}")
    else:
        print(f"No followers of {god_name} found.")

def handle_info_command(parts):
    name = " ".join(parts[:-1])
    character = next((char for char in characters if char.name.lower() == name.lower()), None)
    god = next((g for g in gods if g.name.lower() == name.lower()), None)
    if character:
        print(character.display_info())
    elif god:
        print(god.display_info())
    else:
        print(f"No character or god named {name} found.")

def handle_edit_god_command():
    name = input("Enter the name of the god to edit: ")
    god = next((g for g in gods if g.name.lower() == name.lower()), None)
    if god:
        new_name = input(f"Enter new name ({god.name}): ") or god.name
        new_patronage = input(f"Enter new patronage (comma separated) ({', '.join(god.patronage)}): ").split(", ") or god.patronage
        new_symbols = input(f"Enter new symbols ({god.symbols}): ") or god.symbols
        new_notable_followers = input(f"Enter new notable followers (comma separated) ({', '.join(god.notable_followers)}): ").split(", ") or god.notable_followers
        new_notes = input(f"Enter new notes ({god.notes}): ") or god.notes

        god.name = new_name
        god.patronage = new_patronage
        god.symbols = new_symbols
        god.notable_followers = set(new_notable_followers)
        god.notes = new_notes

        save_to_file(gods, "gods.json")
        print(f"{god.name} has been updated.")
    else:
        print(f"No god named {name} found.")

def handle_edit_character_command():
    name = input("Enter the name of the character to edit: ")
    character = next((char for char in characters if char.name.lower() == name.lower()), None)
    if character:
        new_name = input(f"Enter new name ({character.name}): ") or character.name
        new_race = input(f"Enter new race ({character.race}): ") or character.race
        new_class = input(f"Enter new class ({character.char_class}): ") or character.char_class
        new_level = int(input(f"Enter new level ({character.level}): ") or character.level)
        new_subclass = input(f"Enter new subclass ({character.sub_class}): ") or character.sub_class
        new_ability_modifiers = character.ability_modifiers
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            new_mod = input(f"Enter new {ability} modifier ({character.ability_modifiers[ability]}): ")
            if new_mod:
                new_ability_modifiers[ability] = int(new_mod)
        new_proficiencies = input(f"Enter new proficiencies (comma separated) ({', '.join(character.proficiencies)}): ").split(", ") or character.proficiencies
        new_saving_throws = input(f"Enter new saving throws (comma separated) ({', '.join(character.saving_throws)}): ").split(", ") or character.saving_throws
        new_actions = {
            "bonus_actions": input(f"Enter new bonus actions ({character.actions['bonus_actions']}): ") or character.actions["bonus_actions"],
            "extra_attacks": int(input(f"Enter new extra attacks ({character.actions['extra_attacks']}): ") or character.actions["extra_attacks"]),
            "actions": int(input(f"Enter new actions ({character.actions['actions']}): ") or character.actions["actions"])
        }
        new_god = input(f"Enter new god ({character.god}): ") or character.god
        new_proficiency_bonus = int(input(f"Enter new proficiency bonus ({character.proficiency_bonus}): ") or character.proficiency_bonus)

        character.name = new_name
        character.race = new_race
        character.char_class = new_class
        character.level = new_level
        character.sub_class = new_subclass
        character.ability_modifiers = new_ability_modifiers
        character.proficiencies = new_proficiencies
        character.saving_throws = new_saving_throws
        character.actions = new_actions
        character.god = new_god
        character.proficiency_bonus = new_proficiency_bonus

        save_to_file(characters, "characters.json")
        print(f"{character.name} has been updated.")
    else:
        print(f"No character named {name} found.")

def handle_command(user_input):
    parts = user_input.split()

    if user_input == "quit":
        return False
    elif user_input == "help":
        display_help()
    elif "check" in user_input:
        handle_check_command(parts)
    elif len(parts) >= 3 and parts[-1].lower() == "st":
        handle_st_command(parts)
    elif user_input == "all worships":
        print(list_all_worships())
    elif len(parts) > 1 and parts[-1].lower() == "worship":
        handle_worship_command(parts)
    elif len(parts) > 2 and parts[0].lower() == "god" and parts[1].lower() == "search":
        handle_god_search_command(parts)
    elif len(parts) > 2 and parts[0].lower() == "god" and parts[1].lower() == "of":
        handle_god_of_command(parts)
    elif len(parts) > 1 and parts[-1].lower() == "followers":
        handle_followers_command(parts)
    elif len(parts) > 1 and parts[-1].lower() == "info":
        handle_info_command(parts)
    elif user_input.startswith("edit god"):
        handle_edit_god_command()
    elif user_input.startswith("edit character"):
        handle_edit_character_command()
    elif user_input == "add character":
        handle_add_character_command()
    elif user_input == "add god":
        handle_add_god_command()
    elif user_input == "add shop":
        handle_add_shop_command()
    elif user_input == "add town":
        handle_add_town_command()
    elif user_input == "add shopkeep":
        handle_add_shopkeep_command()
    elif user_input == "add tavern":
        handle_add_tavern_command()
    elif user_input == "all shops":
        handle_all_shops_command()
    elif len(parts) > 1 and parts[-1].lower() == "shops":
        handle_town_shops_command(parts)
    elif len(parts) > 1 and parts[-1].lower() == "taverns":
        handle_town_taverns_command(parts)
    elif len(parts) == 2 and parts[-1].lower() == "taverns":
        handle_town_wealth_taverns_command(parts)
    elif user_input == "bruh":
        print("bruh")
    else:
        print("Unknown command. Please try again.")
    
    return True

def main():
    while True:
        user_input = input("What would you like to do? (type help for a list of commands): ").lower()
        if not handle_command(user_input):
            break

if __name__ == "__main__":
    main()
