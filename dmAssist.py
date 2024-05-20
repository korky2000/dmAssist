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
    
def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump([item.to_dict() for item in data], f, indent=4)

def load_from_file(filename, cls):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [cls.from_dict(item) for item in data]
    except FileNotFoundError:
        return []

def load_characters():
    return load_from_file("characters.json", Character)

def save_characters(characters):
    save_to_file(characters, "characters.json")

def load_gods():
    return load_from_file("gods.json", God)

def save_gods(gods):
    save_to_file(gods, "gods.json")

def load_shops():
    return load_from_file("shops.json", Shop)

def save_shops(shops):
    save_to_file(shops, "shops.json")

def load_towns():
    return load_from_file("towns.json", Town)

def save_towns(towns):
    save_to_file(towns, "towns.json")

characters = load_characters()
gods = load_gods()
shops = load_shops()
towns = load_towns()

def get_best_character_for_stat(skill):
    best_character = None
    highest_stat = -1
    for character in characters:
        char_stat = character.get_stat(skill)
        if char_stat is not None and char_stat > highest_stat:
            highest_stat = char_stat
            best_character = character
    return best_character

def list_all_worships():
    return "\n".join([f"{character.name} worships {character.god}." for character in characters])

def find_character_by_name(name):
    return next((char for char in characters if char.name.lower() == name.lower()), None)

def find_god_by_name(name):
    return next((g for g in gods if g.name.lower() == name.lower()), None)

def character_worship(character_name):
    character = find_character_by_name(character_name)
    if character:
        return f"{character.name} worships {character.god}."
    return f"No character named {character_name} found."

def search_gods(god_name=None):
    if god_name:
        god = find_god_by_name(god_name)
        if god:
            return god.display_info()
        return f"No god named {god_name} found."
    else:
        return "\n".join([god.name for god in gods])

def search_god_of(aspect):
    for god in gods:
        if aspect.lower() in [patron.lower() for patron in god.patronage]:
            return f"The god of {aspect} is {god.name}."
    return f"No god found for the patronage of {aspect}."

def who_worships(god_name):
    worshipers = [character.name for character in characters if character.god.lower() == god_name.lower()]
    if worshipers:
        return f"Characters who worship {god_name}: {', '.join(worshipers)}"
    else:
        return f"No characters worship {god_name}."

def handle_check_command(parts):
    if len(parts) >= 2:
        skill_to_check = " ".join(parts[:-1])
        best_character = get_best_character_for_stat(skill_to_check)
        if best_character:
            print(f"The best character for {skill_to_check} is {best_character.name} with a {skill_to_check} modifier of {best_character.get_stat(skill_to_check)}.")
        else:
            print(f"No character has a stat for {skill_to_check}.")
    else:
        print("Please specify the skill to check (e.g., perception check).")

def handle_worship_command(parts):
    if len(parts) > 1:
        character_name = " ".join(parts[:-1])
        result = character_worship(character_name)
        print(result)
    else:
        print("Please specify the character to check (e.g., Spike worship).")

def handle_god_search_command(parts):
    if len(parts) > 2:
        god_name = " ".join(parts[2:])
        result = search_gods(god_name)
        print(result)
    else:
        result = search_gods()
        print(result)

def handle_god_of_command(parts):
    if len(parts) > 2:
        aspect = " ".join(parts[2:])
        result = search_god_of(aspect)
        print(result)
    else:
        print("Please specify the aspect to search for (e.g., god of greed).")

def handle_followers_command(parts):
    if len(parts) > 1:
        god_name = " ".join(parts[:-1])
        result = who_worships(god_name)
        print(result)
    else:
        print("Please specify the god to check (e.g., Habit Followers).")

def handle_add_character_command():
    try:
        name = input("Enter character's name: ")
        race = input("Enter character's race: ")
        char_class = input("Enter character's class: ")
        level = int(input("Enter character's level: "))
        sub_class = input("Enter character's subclass: ")
        abilities = {}
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            abilities[ability] = int(input(f"Enter {name}'s {ability} modifier: "))
        proficiencies = input(f"Enter {name}'s proficiencies (comma separated): ").lower().split(", ")
        saving_throws = input(f"Enter {name}'s saving throw proficiencies (comma separated): ").lower().split(", ")
        actions = {
            "bonus_actions": input(f"Can {name} perform bonus actions? (True/False): ").lower() == "true",
            "extra_attacks": int(input(f"Enter the number of extra attacks {name} has: ")),
            "actions": int(input(f"Enter the number of actions {name} can perform: "))
        }
        god = input(f"Enter the god {name} worships: ")
        proficiency_bonus = int(input(f"Enter the proficiency bonus for {name}: "))
        
        new_character = Character(name, race, char_class, level, sub_class, abilities, proficiencies, actions, god, proficiency_bonus, saving_throws)
        characters.append(new_character)
        save_characters(characters)
        print(f"{name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_edit_character_command():
    name = input("Enter the name of the character to edit: ")
    character = find_character_by_name(name)
    
    if character:
        print(f"Editing {character.name}.")
        print("Enter the attribute you want to edit (name, race, char_class, level, sub_class, ability_modifiers, proficiencies, saving_throws, actions, god, proficiency_bonus): ")
        attribute = input().lower()

        if attribute == "name":
            character.name = input("Enter new name: ")
        elif attribute == "race":
            character.race = input("Enter new race: ")
        elif attribute == "char_class":
            character.char_class = input("Enter new class: ")
        elif attribute == "level":
            character.level = int(input("Enter new level: "))
        elif attribute == "sub_class":
            character.sub_class = input("Enter new subclass: ")
        elif attribute == "ability_modifiers":
            for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
                character.ability_modifiers[ability] = int(input(f"Enter new {ability} modifier: "))
        elif attribute == "proficiencies":
            character.proficiencies = input("Enter new proficiencies (comma separated): ").lower().split(", ")
        elif attribute == "saving_throws":
            character.saving_throws = input("Enter new saving throws (comma separated): ").lower().split(", ")
        elif attribute == "actions":
            character.actions["bonus_actions"] = input("Can perform bonus actions? (True/False): ").lower() == "true"
            character.actions["extra_attacks"] = int(input("Enter new number of extra attacks: "))
            character.actions["actions"] = int(input("Enter new number of actions: "))
        elif attribute == "god":
            character.god = input("Enter new god: ")
        elif attribute == "proficiency_bonus":
            character.proficiency_bonus = int(input("Enter new proficiency bonus: "))
        else:
            print("Invalid attribute.")

        save_characters(characters)
        print(f"{character.name}'s details have been updated successfully.")
    else:
        print(f"No character named {name} found.")

def handle_add_god_command():
    try:
        name = input("Enter god's name: ")
        patronage = input("Enter god's patronage (comma separated): ").split(", ")
        symbols = input("Enter god's symbols: ")
        notable_followers = input("Enter notable followers (comma separated): ").split(", ")
        notes = input("Enter any additional notes: ")
        
        new_god = God(name, patronage, symbols, set(notable_followers), notes)
        gods.append(new_god)
        save_gods(gods)
        print(f"{name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def save_shopkeeps(shopkeeps):
    save_to_file(shopkeeps, "shopkeeps.json")

def load_shopkeeps():
    return load_from_file("shopkeeps.json", Shopkeep)

def handle_add_shopkeep_command():
    try:
        name = input("Enter shopkeep's name: ")
        town = input("Enter the town where the shopkeep is located: ")
        shop = input("Enter the shop the shopkeep manages: ")
        relationships = input("Enter relationships (comma separated): ").split(", ")
        notes = input("Enter any additional notes: ")

        new_shopkeep = Shopkeep(name, town, shop, relationships, notes)
        shopkeeps.append(new_shopkeep)
        save_shopkeeps(shopkeeps)
        print(f"{name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_edit_shopkeep_command():
    name = input("Enter the name of the shopkeep to edit: ")
    shopkeep = next((sk for sk in shopkeeps if sk.name.lower() == name.lower()), None)
    
    if shopkeep:
        print(f"Editing {shopkeep.name}.")
        print("Enter the attribute you want to edit (name, town, shop, relationships, notes): ")
        attribute = input().lower()

        if attribute == "name":
            shopkeep.name = input("Enter new name: ")
        elif attribute == "town":
            shopkeep.town = input("Enter new town: ")
        elif attribute == "shop":
            shopkeep.shop = input("Enter new shop: ")
        elif attribute == "relationships":
            shopkeep.relationships = input("Enter new relationships (comma separated): ").split(", ")
        elif attribute == "notes":
            shopkeep.notes = input("Enter new notes: ")
        else:
            print("Invalid attribute.")

        save_shopkeeps(shopkeeps)
        print(f"{shopkeep.name}'s details have been updated successfully.")
    else:
        print(f"No shopkeep named {name} found.")

def handle_list_shopkeeps_command():
    if shopkeeps:
        for shopkeep in shopkeeps:
            print(shopkeep.display_info())
    else:
        print("No shopkeeps available.")


def handle_info_command(parts):
    if len(parts) >= 2:
        name = " ".join(parts[:-1])
        character = find_character_by_name(name)
        if character:
            print(character.display_info())
            return
        
        god = find_god_by_name(name)
        if god:
            print(god.display_info())
            return
        
        print(f"No character or god named {name} found.")
        
    else:
        print("Please specify the name to search for (e.g., Spike info).")

def handle_edit_god_command():
    name = input("Enter the name of the god to edit: ")
    god = find_god_by_name(name)
    
    if god:
        print(f"Editing {god.name}.")
        print("Enter the attribute you want to edit (name, patronage, symbols, notable_followers, notes): ")
        attribute = input().lower()

        if attribute == "name":
            god.name = input("Enter new name: ")
        elif attribute == "patronage":
            god.patronage = input("Enter new patronage (comma separated): ").split(", ")
        elif attribute == "symbols":
            god.symbols = input("Enter new symbols: ")
        elif attribute == "notable_followers":
            god.notable_followers = input("Enter new notable followers (comma separated): ").split(", ")
        elif attribute == "notes":
            god.notes = input("Enter new notes: ")
        else:
            print("Invalid attribute.")

        save_gods(gods)
        print(f"{god.name}'s details have been updated successfully.")
    else:
        print(f"No god named {name} found.")

def handle_stat_command(parts):
    if len(parts) == 2:
        character_name, stat = parts[0], parts[1].lower()
        if character_name.lower() == "all":
            for character in characters:
                stat_value = character.get_stat(stat)
                if stat_value is not None:
                    print(f"{character.name}'s {stat.capitalize()}: {stat_value}")
                else:
                    print(f"{character.name} does not have a {stat.capitalize()} stat.")
        else:
            character = find_character_by_name(character_name)
            if character:
                stat_value = character.get_stat(stat)
                if stat_value is not None:
                    print(f"{character.name}'s {stat.capitalize()}: {stat_value}")
                else:
                    print(f"{character.name} does not have a {stat.capitalize()} stat.")
            else:
                print(f"No character named {character_name} found.")
    else:
        print("Please specify the character and stat to check (e.g., Spike Perception or All Perception).")

def handle_st_command(parts):
    if len(parts) >= 3:
        character_name, ability, _ = parts[0], parts[1].lower(), parts[2].lower()
        if character_name.lower() == "all":
            for character in characters:
                st_value = character.get_saving_throws(ability)
                print(f"{character.name}'s {ability.capitalize()} Saving Throw: {st_value}")
        else:
            character = find_character_by_name(character_name)
            if character:
                st_value = character.get_saving_throws(ability)
                print(f"{character.name}'s {ability.capitalize()} Saving Throw: {st_value}")
            else:
                print(f"No character named {character_name} found.")
    elif len(parts) == 2 and parts[0].lower() == "all" and parts[1].lower() == "st":
        for character in characters:
            st_values = {ability.capitalize(): character.get_saving_throws(ability) for ability in character.saving_throws}
            print(f"{character.name}'s Saving Throws: {st_values}")
    else:
        print("Please specify the character and ability for the saving throw (e.g., Spike strength st or All strength st).")

def handle_add_shop_command():
    try:
        name = input("Enter the name: ")
        town = input("Enter the town where the shop is located: ")
        type = input("Enter the type of shop: ")
        shopkeep = input("Enter the name of the shopkeep: ")
        inventory = {}
        while True:
            item = input("Enter item name (or 'done' to finish): ")
            if item.lower() == 'done':
                break
            price = float(input(f"Enter price for {item}: "))
            inventory[item] = price
        
        new_shop = Shop(name, town, type, shopkeep, inventory)
        shops.append(new_shop)
        save_shops(shops)
        print(f"Shop in {town} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_add_town_command():
    try:
        name = input("Enter town name: ")
        mayor = input("Enter mayor's name: ")
        important_guilds = input("Enter important guilds (comma separated): ").split(", ")
        patron_gods = input("Enter patron gods (comma separated): ").split(", ")
        
        new_town = Town(name, mayor, important_guilds, patron_gods)
        towns.append(new_town)
        save_towns(towns)
        print(f"Town {name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_all_shops_command():
    if shops:
        for shop in shops:
            print(shop.display_info())
    else:
        print("No shops available.")

def handle_town_shops_command(parts):
    town = " ".join(parts[:-1])
    town_shops = [shop for shop in shops if shop.town.lower() == town.lower()]
    if town_shops:
        for shop in town_shops:
            print(shop.display_info())
    else:
        print(f"No shops found in {town}.")

def display_help():
    help_text = """
    Available commands:
    - <skill> check: Check the best character for a given skill (e.g., perception check).
    - all worships: List all characters and their gods.
    - <character> worship: Check which god a specific character worships (e.g., Spike worship).
    - god search [<god name>]: Search for information about a specific god (e.g., god search Habit) or list all gods.
    - god of <aspect>: Find the god who is the patron of a given aspect (e.g., god of greed).
    - edit god: Edit a god
    - [god name] Followers: List all characters who worship a specific god (e.g., Habit Followers).
    - <name> info: Display information about a specific character or god (e.g., Spike info).
    - add character: Add a new character to the list.
    - edit character: Edit an existing character.
    - add god: Add a new god to the list.
    - <character> <proficiency/ability>: Get a specific character's proficiency or ability modifier (e.g., Spike Perception).
    - All <proficiency/ability>: Get all characters' proficiency or ability modifiers (e.g., All Perception).
    - <character> <ability> st: Get a specific character's saving throw for an ability (e.g., Spike strength st).
    - All <ability> st: Get all characters' saving throws for an ability (e.g., All strength st).
    - All st: Get all saving throws for all characters.
    - add shop: Add a new shop to the list.
    - add town: Add a new town to the list.
    - all shops: List all shops.
    - [town] shops: List all shops in a specific town.
    - help: Display this help message.
    - quit: Exit the program.
    """
    print(help_text)

def handle_skill_command(parts):
    if len(parts) == 2:
        character_name, skill = parts[0], parts[1].lower()
        character = find_character_by_name(character_name)
        if character:
            skill_value = character.get_stat(skill)
            if skill_value is not None:
                print(f"{character.name}'s {skill.capitalize()} skill value: {skill_value}")
            else:
                print(f"{character.name} does not have a {skill.capitalize()} skill.")
        else:
            print(f"No character named {character_name} found.")
    else:
        print("Please specify the character and skill (e.g., Spike Perception).")

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
    elif user_input == "all shops":
        handle_all_shops_command()
    elif len(parts) > 1 and parts[-1].lower() == "shops":
        handle_town_shops_command(parts)
    elif user_input == "bruh":
        print("bruh")
    elif len(parts) == 2:
        handle_skill_command(parts)

    else:
        print("Unknown command. Please try again.")
    
    return True

def handle_all_shops_command():
    if shops:
        for shop in shops:
            print(shop.display_info())
    else:
        print("No shops available.")

def handle_town_shops_command(parts):
    town_name = " ".join(parts[:-1])
    town_shops = [shop for shop in shops if shop.town.lower() == town_name.lower()]
    if town_shops:
        for shop in town_shops:
            print(shop.display_info())
    else:
        print(f"No shops found in {town_name}.")

characters = load_characters()
gods = load_gods()
shops = load_shops()
towns = load_towns()
shopkeeps = load_shopkeeps()

def main():
    while True:
        user_input = input("What would you like to do? (type help for a list of commands): ").lower()
        if not handle_command(user_input):
            break

if __name__ == "__main__":
    main()
