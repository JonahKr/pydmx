import json
import os

directory = "./"

manufacturers = []

# For export the following structure is created:
# {
#   manufacturerX$fixtureX: {}
# }
#
ofl = {}

# Iterating over OFL
for dirnum, (root, dirs, files) in enumerate(os.walk(directory, topdown=True)):
    # First Directory is the Directory containing the different manufacturers
    if dirnum == 0:
        manufacturers = dirs
        continue

    for file in files:
        content = open(os.path.join(root, file), encoding="utf-8")
        parsed_content = json.load(content)
        manufacturer = parsed_content["manufacturerKey"]
        fixture = parsed_content["fixtureKey"]
        ofl[manufacturer + "#" + fixture] = parsed_content

ofl["_manufacturers"] = manufacturers

with open("ofl.json", "w") as outfile:
    json.dump(ofl, outfile)
