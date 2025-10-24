import tkinter as tk
from tkinter import messagebox
import csv
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Calculate BMI from weight (kg) and height (m)
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Determine BMI category based on BMI value
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Save BMI record to CSV file
def save_data(name, weight, height, bmi, category):
    file_exists = os.path.exists("bmi_data.csv")
    with open("bmi_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file doesn’t exist yet
            writer.writerow(["Date", "Name", "Weight", "Height", "BMI", "Category"])
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            weight,
            height,
            bmi,
            category
        ])

# Handle submit button click
def submit():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if not name or weight <= 0 or height <= 0:
            raise ValueError("Invalid input")

        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        result_label.config(
            text=f"{name}, your BMI is {bmi} ({category})",
            bg="#2c3e50",
            fg="white"
        )

        save_data(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid name, weight, and height.")

# Plot BMI trend for a specific user
def plot_bmi_with_categories(user_data, user_name=None):
    user_data = user_data.copy()
    user_data["Date"] = pd.to_datetime(user_data["Date"])
    user_data = user_data.sort_values("Date")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw background bands for BMI categories
    ax.axhspan(0, 18.5, color="#87CEEB", alpha=0.3, label="Underweight")
    ax.axhspan(18.5, 25, color="#90EE90", alpha=0.3, label="Normal")
    ax.axhspan(25, 30, color="#FFD700", alpha=0.3, label="Overweight")
    ax.axhspan(30, 50, color="#FF4500", alpha=0.3, label="Obese")

    # Plot BMI line for user
    ax.plot(user_data["Date"], user_data["BMI"], marker='o', color="#004080", linewidth=2)

    # Format x-axis dates
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)

    ax.set_xlabel("Date")
    ax.set_ylabel("BMI")
    ax.set_ylim(10, 40)

    title = f"BMI Trend for {user_name}" if user_name else "BMI Trend"
    ax.set_title(title, fontsize=14, fontweight="bold")

    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.show()

# Plot BMI trends for all users on the same graph
def plot_bmi_all_users(data):
    data = data.copy()
    data["Date"] = pd.to_datetime(data["Date"])

    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw background bands for BMI categories
    ax.axhspan(0, 18.5, color="#87CEEB", alpha=0.3, label="Underweight")
    ax.axhspan(18.5, 25, color="#90EE90", alpha=0.3, label="Normal")
    ax.axhspan(25, 30, color="#FFD700", alpha=0.3, label="Overweight")
    ax.axhspan(30, 50, color="#FF4500", alpha=0.3, label="Obese")

    # Plot a line for each user
    for user in data["Name"].unique():
        user_df = data[data["Name"].str.strip().str.lower() == user.strip().lower()]
        user_df = user_df.sort_values("Date")
        ax.plot(user_df["Date"], user_df["BMI"], marker='o', linewidth=2, label=user)

    # Format x-axis dates
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)

    ax.set_xlabel("Date")
    ax.set_ylabel("BMI")
    ax.set_ylim(10, 40)
    ax.set_title("BMI Trends for All Users", fontsize=14, fontweight="bold")

    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", fontsize=8)

    plt.tight_layout()
    plt.show()

# Show history button handler: plot all users’ BMI trends
def show_history():
    if not os.path.exists("bmi_data.csv"):
        messagebox.showinfo("No Data", "No BMI data found yet.")
        return

    data = pd.read_csv("bmi_data.csv")

    if data.empty:
        messagebox.showinfo("No Data", "No BMI data found yet.")
        return

    plot_bmi_all_users(data)

# Analyze button handler: plot selected user’s BMI trend
def analyze_trends():
    if not os.path.exists("bmi_data.csv"):
        messagebox.showinfo("No Data", "No BMI data found yet.")
        return

    data = pd.read_csv("bmi_data.csv")
    name = trend_entry.get().strip()

    if not name:
        messagebox.showinfo("Input Required", "Please enter a name to analyze.")
        return

    user_data = data[data["Name"].str.strip().str.lower() == name.lower()]

    if user_data.empty:
        messagebox.showinfo("No Data", f"No data found for user: {name}")
        return

    plot_bmi_with_categories(user_data, user_name=name)

# -------------------- GUI Setup --------------------

window = tk.Tk()
window.title("Advanced BMI Calculator")
window.geometry("480x480")
window.configure(bg="#f0f0f0")

# Input fields
frame = tk.Frame(window, bg="#f0f0f0")
frame.pack(pady=15)

tk.Label(frame, text="Name:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(frame, font=("Arial", 12))
name_entry.grid(row=0, column=1, pady=5, ipadx=50)

tk.Label(frame, text="Weight (kg):", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
weight_entry = tk.Entry(frame, font=("Arial", 12))
weight_entry.grid(row=1, column=1, pady=5, ipadx=50)

tk.Label(frame, text="Height (m):", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
height_entry = tk.Entry(frame, font=("Arial", 12))
height_entry.grid(row=2, column=1, pady=5, ipadx=50)

# Calculate button
calc_btn = tk.Button(window, text="Calculate BMI", bg="#e67e22", fg="white", font=("Arial", 12, "bold"), relief="flat", command=submit)
calc_btn.pack(pady=10, ipadx=10, ipady=5)

# Result display label
result_label = tk.Label(window, text="", bg="#f0f0f0", font=("Arial", 13), justify="center", relief="groove", bd=2, padx=20, pady=10, width=40)
result_label.pack(pady=10)

# Show all users' BMI history button
history_btn = tk.Button(window, text="Show BMI History (All Users)", bg="#7f8c8d", fg="white", font=("Arial", 12, "bold"), relief="flat", command=show_history)
history_btn.pack(pady=5, ipadx=10, ipady=5)

# Separator line
separator = tk.Frame(window, height=2, bd=1, relief="sunken", bg="#bdc3c7")
separator.pack(fill="x", padx=30, pady=15)

# Trend analysis section
trend_frame = tk.Frame(window, bg="#f0f0f0")
trend_frame.pack()

tk.Label(trend_frame, text="Enter Name to Analyze:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
trend_entry = tk.Entry(trend_frame, font=("Arial", 12))
trend_entry.grid(row=0, column=1, pady=5, ipadx=50)

analyze_btn = tk.Button(trend_frame, text="Analyze Trends", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), relief="flat", command=analyze_trends)
analyze_btn.grid(row=1, column=0, columnspan=2, pady=15, ipadx=10, ipady=5)

window.mainloop()
