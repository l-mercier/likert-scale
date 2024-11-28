import tkinter as tk
from tkinter import messagebox
import csv
import numpy as np
from datetime import datetime
# Path to save the CSV file
folder = 'your_folder/'
file_path = 'user_responses.csv'

# Get the current date
current_time = datetime.now()
date = current_time.date()

agremement_5labels = {1:'Strongly disagree',
                     2:'Disagree',
                     3:'Neutral',
                     4:'Agree',
                     5:'Strongely Agree'}

agremement_7labels = {1:'Strongly disagree',
                     2:'Disagree',
                     3:'Somewhat disagree',
                     4:'Neutral',
                     5:'Somewhat agree',
                     6:'Agree',
                     7:'Strongely Agree'}

likelihood_5labels = {1:'Very unlikely',
                     2:'Unlikely',
                     3:'Neutral',
                     4:'Likely',
                     5:'Very likely'}

satisfaction_5labels = {1:'Extremely dissatisfied',
                     2:'Disatisfied',
                     3:'Neutral',
                     4:'Satisfied',
                     5:'Extremely satisfied'}

frequency_5labels = {1:'Never',
                     2:'Rarely',
                     3:'Sometimes',
                     4:'Often',
                     5:'Very often'}

importance_5labels = {1:'Not at all important',
                     2:'Of little importance',
                     3:'Of average importance',
                     4:'Very important',
                     5:'Essential'}

## Create new labels for your specific use case as needed.



# Likert-scale nb of points
nb_points = 7

# List of questions
questions = [
    'What did you think of ...',  # related theme
    'Do you think ... ?', 
    'Do you agree with ... ?',
    'Are you aware that ... ?'
]

font_settings = ("Helvetica", 15, "bold")

# Initialize variables for storing scale values
scales = []

# Function to save the data to a CSV file
def save_data():
    user_id = user_id_entry.get()
    responses = [scale.get() for scale in scales]

    # Ensure the user has provided an ID and answered both questions
    if not user_id:
        messagebox.showerror("Error", "Please enter your ID.")
        return

    if any(response == 0 for response in responses):        
        messagebox.showerror("Error", f"Please answer to the {len(questions)} questions")
        return

    # Open the CSV file and append the user's responses
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header if the file is empty
        if file.tell() == 0:
            writer.writerow(['ID'] + ['time'] + [f'Q{i + 1}' for i in range(len(questions))])
        writer.writerow([user_id] + [current_time] + responses)

    # Show confirmation
    messagebox.showinfo("Submit successful", "Your replies were saved !")

    # Clear input fields for next user
    user_id_entry.delete(0, tk.END)
    for scale in scales:
        scale.set(np.trunc(nb_points/2)+1)  # Reset to neutral

# Create the main window
root = tk.Tk()
root.title("Questionnaire")
root.geometry("800x500")  # Set a larger window size for better appearance

# Define the string labels for the Likert scale
if nb_points == 5 :
    string_values = {
        1: "Pas du tout",
        2: "Moyennement",
        3: "Neutre",
        4: "Beaucoup",
        5: "Totalement"
    }

if nb_points == 7 :
    string_values = {
        1: "Pas du tout",
        2: "Un peu",
        3: "Moyennement",
        4: "Neutre",
        5: "Assez",
        6: "Beaucoup",
        7: "Totalement"
    }

# User ID entry
tk.Label(root, text="Entrez votre ID:").pack(anchor="w", padx=10, pady=5)
user_id_entry = tk.Entry(root)
user_id_entry.pack(fill="x", padx=10, pady=5)

# Dynamically create scales for each question
for idx, question in enumerate(questions):
    # Question label
    tk.Label(root, text=question, font=font_settings).pack(anchor="center", padx=10, pady=5)
    
    # Scale
    scale_var = tk.IntVar()
    scale_var.set(np.trunc(nb_points/2)+1)  # Default to neutral
    scales.append(scale_var)
    scale = tk.Scale(root, from_=1, to=nb_points, orient=tk.HORIZONTAL, variable=scale_var, showvalue=0)
    scale.pack(fill="x", padx=10, pady=5)
    
    # Scale labels
    scale_frame = tk.Frame(root)
    scale_frame.pack(fill="x", padx=10)
    for i, label in string_values.items():
        if i == 1:  # Leftmost label
            tk.Label(scale_frame, text=label, anchor="w").pack(side="left", padx=(0, 5), fill="both", expand=True)
        elif i == nb_points:  # Rightmost label
            tk.Label(scale_frame, text=label, anchor="e").pack(side="right", padx=(5, 0), fill="both", expand=True)
        else:  # Centered labels
            tk.Label(scale_frame, text=label, anchor="center").pack(side="left", expand=True)

# Submit button
submit_button = tk.Button(root, text="Submit", command=save_data)
submit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
