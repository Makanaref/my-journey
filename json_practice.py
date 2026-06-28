import json

person = {
    "name": "Donk",
    "age": 20,
    "skills": ["Git", "Python"],
    "active": True
}

with open("person.json", "w") as f:
    json.dump(person, f, indent=4)

print("Saved to person.json!")

with open("person.json", "r") as f:
    loaded = json.load(f)

print("\n--- Loaded Data ---")
print("Name:", loaded["name"])
print("Skills:", loaded["skills"])
print("First skill:", loaded["skills"][0])