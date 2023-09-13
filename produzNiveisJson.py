import json

data = {}
value = 100
percentage_increment = 0.05  # Incremento de 5% a cada valor

for key in range(1, 151):
    data[key] = round(value, 2)
    value += int(value * percentage_increment)

json_data = json.dumps(data, indent=4)

with open('output.json', 'w') as f:
    f.write(json_data)
