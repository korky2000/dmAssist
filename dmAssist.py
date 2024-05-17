#!/usr/bin/env python3

import json

class Character:
    def __init__(self, name, race, char_class, level, sub_class, ability_modifiers, proficiencies, actions, god):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.sub_class = sub_class
        self.ability_modifiers = ability_modifiers
        self.proficiencies = proficiencies
        self.actions = actions
        self.god = god

    def calculate_proficiency_bonus(self):
        if 1 <= self.level <= 4:
            return 2
        elif 5 <= self.level <= 8:
            return 3
        elif 9 <= self.level <= 12:
            return 4
        elif 13 <= self.level <= 16:
            return 5
        elif 17 <= self.level <= 20:
            return 6
        else:
            return 0

    def get_stat(self, stat):
        if stat.lower() in self.ability_modifiers:
            return self.ability_modifiers[stat.lower()]
        
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

        ability = skill_to_ability.get(stat.lower(), None)
        if not ability:
            return None

        ability_modifier = self.ability_modifiers.get(ability, 0)
        total_modifier = ability_modifier

        if stat.lower() in self.proficiencies:
            total_modifier += self.calculate_proficiency_bonus()

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
            "god": self.god
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
            data["god"]
        )

    def display_info(self):
        info = f"""
        Name: {self.name}
        Race: {self.race}
        Class: {self.char_class}
        Level: {self.level}
        Subclass: {self.sub_class}
        Ability Modifiers: {self.ability_modifiers}
        Proficiencies: {', '.join(self.proficiencies)}
        Actions: {self.actions}
        God: {self.god}
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
        Name: {self.name}
        Patronage: {', '.join(self.patronage)}
        Symbols: {self.symbols}
        Notable Followers: {', '.join(self.notable_followers)}
        Notes: {self.notes}
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

characters = load_characters()
gods = load_gods()

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

def character_worship(character_name):
    character = find_character_by_name(character_name)
    if character:
        return f"{character.name} worships {character.god}."
    return f"No character named {character_name} found."

def search_gods(god_name=None):
    if god_name:
        god = next((g for g in gods if g.name.lower() == god_name.lower()), None)
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
        skill_to_check = " ".join(parts[:-1])  # e.g., "perception" from "perception check"
        best_character = get_best_character_for_stat(skill_to_check)
        if best_character:
            print(f"The best character for {skill_to_check} is {best_character.name} with a {skill_to_check} modifier of {best_character.get_stat(skill_to_check)}.")
        else:
            print(f"No character has a stat for {skill_to_check}.")
    else:
        print("Please specify the skill to check (e.g., perception check).")

def handle_worship_command(parts):
    if len(parts) > 1:
        character_name = " ".join(parts[:-1])  # e.g., "Spike" from "Spike worship"
        result = character_worship(character_name)
        print(result)
    else:
        print("Please specify the character to check (e.g., Spike worship).")

def handle_god_search_command(parts):
    if len(parts) > 2:
        god_name = " ".join(parts[2:])  # e.g., "Habit" from "god search Habit"
        result = search_gods(god_name)
        print(result)
    else:
        result = search_gods()
        print(result)

def handle_god_of_command(parts):
    if len(parts) > 2:
        aspect = " ".join(parts[2:])  # e.g., "greed" from "god of greed"
        result = search_god_of(aspect)
        print(result)
    else:
        print("Please specify the aspect to search for (e.g., god of greed).")

def handle_followers_command(parts):
    if len(parts) > 1:
        god_name = " ".join(parts[:-1])  # e.g., "Habit" from "Habit Followers"
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
        proficiencies = input(f"Enter {name}'s proficiencies (comma separated): ").split(", ")
        actions = {
            "bonus_actions": input(f"Can {name} perform bonus actions? (True/False): ").lower() == "true",
            "extra_attacks": int(input(f"Enter the number of extra attacks {name} has: ")),
            "actions": int(input(f"Enter the number of actions {name} can perform: "))
        }
        god = input(f"Enter the god {name} worships: ")
        
        new_character = Character(name, race, char_class, level, sub_class, abilities, proficiencies, actions, god)
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
        print("Enter the attribute you want to edit (name, race, char_class, level, sub_class, ability_modifiers, proficiencies, actions, god): ")
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
            character.proficiencies = input("Enter new proficiencies (comma separated): ").split(", ")
        elif attribute == "actions":
            character.actions["bonus_actions"] = input("Can perform bonus actions? (True/False): ").lower() == "true"
            character.actions["extra_attacks"] = int(input("Enter new number of extra attacks: "))
            character.actions["actions"] = int(input("Enter new number of actions: "))
        elif attribute == "god":
            character.god = input("Enter new god: ")
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

def handle_info_command(parts):
    if len(parts) >= 2:
        name = " ".join(parts[:-1])  # e.g., "Spike" from "Spike info"
        character = find_character_by_name(name)
        if character:
            print(character.display_info())
            return
        
        god = next((g for g in gods if g.name.lower() == name.lower()), None)
        if god:
            print(god.display_info())
            return
        
        print(f"No character or god named {name} found.")
    else:
        print("Please specify the name to search for (e.g., Spike info).")

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

def display_help():
    help_text = """
    Available commands:
    - <skill> check: Check the best character for a given skill (e.g., perception check).
    - all worships: List all characters and their gods.
    - <character> worship: Check which god a specific character worships (e.g., Spike worship).
    - god search [<god name>]: Search for information about a specific god (e.g., god search Habit) or list all gods.
    - god of <aspect>: Find the god who is the patron of a given aspect (e.g., god of greed).
    - [god name] Followers: List all characters who worship a specific god (e.g., Habit Followers).
    - <name> info: Display information about a specific character or god (e.g., Spike info).
    - add character: Add a new character to the list.
    - edit character: Edit an existing character.
    - add god: Add a new god to the list.
    - <character> <proficiency/ability>: Get a specific character's proficiency or ability modifier (e.g., Spike Perception).
    - All <proficiency/ability>: Get all characters' proficiency or ability modifiers (e.g., All Perception).
    - help: Display this help message.
    - quit: Exit the program.
    """
    print(help_text)

def handle_command(user_input):
    parts = user_input.split()
    command = parts[-1]
    
    if user_input == "quit":
        return False
    elif user_input == "help":
        display_help()
    elif "check" in user_input:
        handle_check_command(parts)
    elif user_input == "all worships":
        print(list_all_worships())
    elif command == "worship" and len(parts) > 1:
        handle_worship_command(parts)
    elif command == "search" and len(parts) > 2 and parts[1] == "god":
        handle_god_search_command(parts)
    elif parts[0] == "god" and parts[1] == "of":
        handle_god_of_command(parts)
    elif command == "followers":
        handle_followers_command(parts)
    elif command == "info":
        handle_info_command(parts)
    elif user_input == "add character":
        handle_add_character_command()
    elif user_input == "edit character":
        handle_edit_character_command()
    elif user_input == "add god":
        handle_add_god_command()
    elif len(parts) == 2:
        handle_stat_command(parts)
    else:
        print("Unknown command. Please try again.")
    
    return True

def main():
    while True:
        user_input = input("What would you like to do? (e.g., perception check, all worships, Spike worship, god search Habit, god of greed, Habit Followers, Spike info, add character, edit character, add god, help, quit): ").lower()
        if not handle_command(user_input):
            break

if __name__ == "__main__":
    main()
