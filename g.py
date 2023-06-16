import json

# Load the JSON file
with open('output/all_data.json', 'r') as file:
    data = json.load(file)

# Filter data and check for non-empty phone numbers
phone_numbers = []
for item in data:
    if 'phone' in item and item['phone'] != "":
        phone_numbers.append(item['phone'])

# Print the phone numbers
for number in phone_numbers:
    print(number)
