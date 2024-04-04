with open("t20_practice.csv", "r") as f:
    lines = f.readlines()

new_lines = [lines[0]]
for line in lines[1:]:
    for i in range(100):
        new_lines.append(line)

with open("temp.csv", "a") as f:
    f.write(new_lines[0])
    for line in new_lines[1:]:
        f.write(line)