d = {"jaipur": "India", "Punjab": "India", "califonia": "USA", "soul": "Korea"}

country = dict()

for city, nation in d.items():
    # If the nation is not yet a key in our new dictionary, initialize it with an empty list
    if nation not in country:
        country[nation] = []
    # Append the city to the nation's list
    country[nation].append(city)

print(country)