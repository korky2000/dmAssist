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

        # Calculate proficiency bonus based on character level
        self.proficiency_bonus = self.calculate_proficiency_bonus()

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
            total_modifier += self.proficiency_bonus

        return total_modifier

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

def display_help():
    help_text = """
    Available commands:
    - <skill> check: Check the best character for a given skill (e.g., perception check).
    - all worships: List all characters and their gods.
    - <character> worship: Check which god a specific character worships (e.g., Spike worship).
    - god search [<god name>]: Search for information about a specific god (e.g., god search Habit) or list all gods.
    - patronage <aspect>: Find the god who is the patron of a given aspect (e.g., patronage greed).
    - help: Display this help message.
    - quit: Exit the program.
    """
    print(help_text)

def main():
    while True:
        user_input = input("What would you like to do? (e.g., perception check, all worships, Spike worship, god search Habit, patronage greed, help, quit): ").lower()
        if user_input == "quit":
            break
        elif user_input == "help":
            display_help()
        elif "check" in user_input:
            parts = user_input.split()
            if len(parts) >= 2:
                skill_to_check = " ".join(parts[:-1])  # e.g., "perception" from "perception check"
                best_character = get_best_character_for_stat(skill_to_check)
                if best_character:
                    print(f"The best character for {skill_to_check} is {best_character.name} with a {skill_to_check} modifier of {best_character.get_stat(skill_to_check)}.")
                else:
                    print(f"No character has a stat for {skill_to_check}.")
            else:
                print("Please specify the skill to check (e.g., perception check).")
        elif user_input == "all worships":
            result = all_worships()
            print(result)
        elif "worship" in user_input:
            parts = user_input.split()
            if len(parts) > 1:
                character_name = " ".join(parts[:-1])  # e.g., "Spike" from "Spike worship"
                result = character_worship(character_name)
                print(result)
            else:
                print("Please specify the character to check (e.g., Spike worship).")
        elif "god search" in user_input:
            parts = user_input.split()
            if len(parts) > 2:
                god_name = " ".join(parts[2:])  # e.g., "Habit" from "god search Habit"
                result = search_gods(god_name)
                print(result)
            else:
                result = search_gods()
                print(result)
        elif "patronage" in user_input:
            parts = user_input.split()
            if len(parts) > 1:
                aspect = " ".join(parts[1:])  # e.g., "greed" from "patronage greed"
                result = search_patronage(aspect)
                print(result)
            else:
                print("Please specify the aspect to search for (e.g., patronage greed).")
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
