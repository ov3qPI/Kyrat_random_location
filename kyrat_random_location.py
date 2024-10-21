import random

# List of Kyrat Locations
locations = {
    'South': [
        "Baghadur", "Varshakot", "Banapur", "Chal Jama Monastery", "City of Pain", "Ghale Homestead",
        "Golden Path Camp", "King's Bridge", "Kyra Tea Factory", "Rochan Brick Factory", "Shanath",
        "The Sleeping Saints", "Tirtha", "Barnali's Textiles", "Kheta Manor", "Khilana Bazaar",
        "Kyra Tea Terraces", "Kyra Tea Weigh Station", "Open Hearts Clinic", "Pranijagat School",
        "Rochan Brick Co. Shipping", "Rochan Brick Co. Storage", "Royal Raksi Brewery", "Seven Treasures Ashram",
        "Shanath Breeders", "Shanath Training Ground", "Abandoned Jheel", "Aghori Ashram", "Arjun's Still",
        "Army Supply Flight 2412", "Army Supply Flight 2707", "Army Supply Flight 2911", "Avinash Primary School",
        # truncated for brevity
    ],
    'North': [
        "Rajgad Gulag", "Ratu Gadhi", "Jalendu Temple", "KEO Svargiya Mine", "Royal Fortress", "Royal Palace",
        "Utkarsh", "Bhirabata Outpost", "Border Observation Post", "KEO Gold Storage", "KEO Logging Camp",
        "KEO Pradhana Mine", "Lhumtse Barracks", "Namboche Monastery", "Pokhari Ghara", "Royal Guard Kennels",
        "Sahi Jile Checkpoint", "Shikharpur", "Altar of Kalinag", "Anadekhi Ruins", "Ananta Muna Shrine",
        "Anjali's Bakery", "Asru Cave", "Asthi Den", "Banashur Ki Sirhi", "Banashur's Refuge", "Banashur's Tranquility",
        # truncated for brevity
    ]
}

def generate_location(region=None):
    if region in locations:
        return random.choice(locations[region])
    else:
        all_locations = [loc for locs in locations.values() for loc in locs]
        return random.choice(all_locations)

def main():
    print('For South, enter "S"')
    print('For North, enter "N"')
    print('For either, press "Enter"')

    region_choice = input("Please choose a region: ").upper()

    if region_choice == 'S':
        region = 'South'
    elif region_choice == 'N':
        region = 'North'
    elif region_choice == '':
        region = None
    else:
        print("Invalid input. Please enter 'S', 'N', or press 'Enter'.")
        return

    location = generate_location(region)
    print(location)

if __name__ == "__main__":
    main()
