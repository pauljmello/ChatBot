# Insert normal .txt/.csv path here
file = open(r"E:\School\San Jose\Fall 2021\CMPE 252\Chat Bot Project\data\TickerNames.txt", "r")

# Splits each row
lines = file.read().splitlines()
n = 0

# Insert target output path here
file2 = open(r"E:\School\San Jose\Fall 2021\CMPE 252\Chat Bot Project\data\TickerNamesYml.yml", "w")

# Writes the headers(?), remember to change the lookup name
file2.write("version: \"3.0\"\nnlu:\n  - lookup: ticker_symbol  \n    examples: |\n")

# Adds indent and dash to each line
for line in lines:
    file2.write("      - " + str(line) + "\n")

# Closes the files
file.close()
file2.close()


# Taken from Online Forum  https://forum.rasa.com/t/lookup-tables-configuration-problem/43359 