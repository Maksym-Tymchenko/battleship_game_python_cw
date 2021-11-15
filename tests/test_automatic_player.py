import os

# Create empty results file
os.system("echo '' > simulation_results.txt")

# Run random vs automatic simulation 100 times
num_simulations = 100
for i in range(num_simulations):
    os.system("python3 main.py 4 >> simulation_results.txt")

# Check how many times Bob (Automatic) won
file = open("simulation_results.txt", "r")
# Read content of file to string
data = file.read()
# Get number of times Bob won
occurrences = data.count("Bob (Automatic) WINS THE GAME")
print(f"My automatic player Bob won {occurrences} times out of {num_simulations}!")