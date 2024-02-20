import os
import subprocess
import time

# Get the current directory where the launcher script is located
current_directory = os.path.dirname(os.path.abspath(__file__))
print("Current Directory:", current_directory)

# List all files in the current directory
files_to_run = [
    "./code/main/parse_GB_raw_data.py",
    "./code/main/parse_SPF_raw_data.py",
    "./code/main/scrape_FRED_data.py",
    "./code/main/annual_forecasts.py",
    "./code/main/compute_abs_error.py",
    "./code/main/abse_reg.py"
]

# Measure the start time
start_time = time.time()

# Run each Python script in the directory
for python_file in files_to_run:
    if python_file != "reproduce.py":  # Exclude the launcher script itself
        subprocess.run(["python", python_file])

end_time = time.time()

# Calculate and print the total runtime
runtime = end_time - start_time
print(f"Total runtime: {runtime:.2f} seconds")






