import sqlite3
con = sqlite3.connect("DnD")
import random

def create_character():
    character = {}

    # Name input
    character['name'] = input("Enter character name: ")

    # Race and race variant
    race_num = random.randint(1, 12)
    character['race'] = f"Race {race_num}"

    race_variant_num = random.randint(1, 4)
    character['race_variant'] = f"Variant {race_variant_num}"

    # Special
    character['special'] = input("Enter special ability/feature: ")

    # Level input or random
    level_input = input("Enter level (or press Enter for random): ")
    character['level'] = int(level_input) if level_input.isdigit() else random.randint(1, 20)

    # Stats
    stats = ['strength', 'intelligence', 'perception', 'constitution', 'dexterity', 'wisdom', 'charisma']
    character['stats'] = {stat: random.randint(1, 20) for stat in stats}

    # Powers
    character['powers'] = input("Enter powers (comma-separated): ").split(',')

    # Inventory
    character['inventory'] = input("Enter inventory items (comma-separated): ").split(',')

    # Language
    character['language'] = input("Enter language(s): ")

    # Personality
    character['personality'] = input("Describe the character's personality: ")

    # Traits (race dependent placeholder)
    character['traits'] = f"Traits based on {character['race']}"

    return character

# Example usage:
my_character = create_character()
print("\nCharacter Sheet:")
for key, value in my_character.items():
    print(f"{key.capitalize()}: {value}")
