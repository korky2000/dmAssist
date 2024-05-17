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

    def get_stat(self, skill):
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
            "social interaction": "charisma"  # Example custom skill
        }

        ability = skill_to_ability.get(skill, None)
        if not ability:
            return None  # If the skill is not found in skill_to_ability

        ability_modifier = self.ability_modifiers.get(ability, 0)
        total_modifier = ability_modifier

        if skill in self.proficiencies:
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

class God:
    def __init__(self, name, patronage, symbols, notable_followers, notes):
        self.name = name
        self.patronage = patronage
        self.symbols = symbols
        self.notable_followers = notable_followers
        self.notes = notes

characters = [
    Character(
        name="Spike",
        race="Dragonborn",
        char_class="Paladin",
        level=3,
        sub_class="Oath of Ancients",
        ability_modifiers={"strength": 3, "dexterity": 2, "constitution": 2, "intelligence": 1, "wisdom": 1, "charisma": 4},
        proficiencies=["intimidation", "persuasion"],
        actions={"bonus_actions": True, "extra_attacks": 1, "actions": 2},
        god="Habit"
    ),
    Character(
        name="Gandalf",
        race="Human",
        char_class="Wizard",
        level=3,
        sub_class="School of Divination",
        ability_modifiers={"strength": 1, "dexterity": 2, "constitution": 3, "intelligence": 5, "wisdom": 4, "charisma": 3},
        proficiencies=["arcana", "history"],
        actions={"bonus_actions": True, "extra_attacks": 0, "actions": 1},
        god="Iluvatar"
    )
]

gods = [
    God(
        name="Habit",
        patronage=["chaos", "entropy", "greed"],
        symbols="Rabbits",
        notable_followers={"Spike", "Asmodeus"},
        notes="Habit has a pet snake named Nigel"
    ),
    God(
        name="Iluvatar",
        patronage=["creation", "life"],
        symbols="Tree",
        notable_followers={"Gandalf", "Frodo"},
        notes="Iluvatar is the all-father of creation"
    )
]

def save_characters_to_file(filename="characters.json"):
    with open(filename, "w") as f:
        json.dump([character.to_dict() for character in characters], f, indent=4)

def load_characters_from_file(filename="characters.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [Character.from_dict(char) for char in data]
    except FileNotFoundError:
        return []

characters = load_characters_from_file()

def get_best_character_for_stat(skill):
    best_character = None
    highest_stat = -1
    for character in characters:
        char_stat = character.get_stat(skill)
        if char_stat is not None and char_stat > highest_stat:
            highest_stat = char_stat
            best_character = character
    return best_character

def all_worships():
    return "\n".join([f"{character.name} worships {character.god}." for character in characters])

def character_worship(character_name):
    for character in characters:
        if character.name.lower() == character_name.lower():
            return f"{character.name} worships {character.god}."
    return f"No character named {character_name} found."

def search_gods(god_name=None):
    if god_name:
        for god in gods:
            if god.name.lower() == god_name.lower():
                return (f"{god.name}: Patronage - {', '.join(god.patronage)}, Symbols - {god.symbols}, "
                        f"Notable Followers - {', '.join(god.notable_followers)}, Notes - {god.notes}")
        return f"No god named {god_name} found."
    else:
        return "\n".join([god.name for god in gods])

def search_patronage(aspect):
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

def handle_patronage_command(parts):
    if len(parts) > 1:
        aspect = " ".join(parts[1:])  # e.g., "greed" from "patronage greed"
        result = search_patronage(aspect)
        print(result)
    else:
        print("Please specify the aspect to search for (e.g., patronage greed).")

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
        save_characters_to_file()
        print(f"{name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def display_help():
    help_text = """
    Available commands:
    - <skill> check: Check the best character for a given skill (e.g., perception check).
    - all worships: List all characters and their gods.
    - <character> worship: Check which god a specific character worships (e.g., Spike worship).
    - god search [<god name>]: Search for information about a specific god (e.g., god search Habit) or list all gods.
    - patronage <aspect>: Find the god who is the patron of a given aspect (e.g., patronage greed).
    - [god name] Followers: List all characters who worship a specific god (e.g., Habit Followers).
    - add character: Add a new character to the list.
    - help: Display this help message.
    - quit: Exit the program.
    """
    print(help_text)

def main():
    while True:
        user_input = input("What would you like to do? (e.g., perception check, all worships, Spike worship, god search Habit, patronage greed, Habit Followers, add character, help, quit): ").lower()
        parts = user_input.split()
        command = parts[-1]
        
        if user_input == "quit":
            break
        elif user_input == "help":
            display_help()
        elif "check" in user_input:
            handle_check_command(parts)
        elif user_input == "all worships":
            print(all_worships())
        elif command == "worship" and len(parts) > 1:
            handle_worship_command(parts)
        elif command == "search" and len(parts) > 2 and parts[1] == "god":
            handle_god_search_command(parts)
        elif command == "patronage":
            handle_patronage_command(parts)
        elif command == "followers":
            handle_followers_command(parts)
        elif user_input == "add character":
            handle_add_character_command()
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
