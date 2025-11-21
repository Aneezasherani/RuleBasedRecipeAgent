import pandas as pd
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json

# Load dataset
try:
    df = pd.read_csv('recipes.csv')
except:
    df = pd.DataFrame(columns=["Recipe Name", "Ingredients", "Steps", "Cuisine", "Meal Type", "Prep Time", "Cook Time", "Total Time", "Calories"])

fav_file = "favorites.json"

# ---------------- FAVORITES ----------------
def load_favorites():
    try:
        with open(fav_file, "r") as f:
            return json.load(f)
    except:
        return []

def save_favorite(recipe):
    favs = load_favorites()
    if recipe not in favs:
        favs.append(recipe)
        with open(fav_file, "w") as f:
            json.dump(favs, f, indent=4)

# ---------------- MATCH LOGIC (FIXED) ----------------
def match_recipes(user_ing):
    exact = []
    partial = []

    user_set = set(user_ing)

    for _, row in df.iterrows():
        recipe_ing = [i.strip().lower() for i in str(row['Ingredients']).split(",")]
        recipe_set = set(recipe_ing)

        match_count = len(user_set & recipe_set)

        # FIXED EXACT MATCH LOGIC
        if recipe_set.issubset(user_set):
            exact.append(row)

        elif match_count > 0:
            missing = list(recipe_set - user_set)
            partial.append((row, missing, match_count))

    partial.sort(key=lambda x: x[2], reverse=True)
    return exact, partial

# ---------------- GUI FUNCTIONS ----------------
def search_recipes():
    user_input = entry.get().lower().strip()
    if not user_input:
        messagebox.showwarning("⚠ Empty Field", "Please enter at least one ingredient.")
        return

    user_ing = [i.strip() for i in user_input.split(",")]
    exact, partial = match_recipes(user_ing)

    result_box.configure(state='normal')
    result_box.delete(1.0, tk.END)

    # EXACT MATCHES
    if exact:
        result_box.insert(tk.END, " Exact Match Recipes \n\n")
        for r in exact:
            result_box.insert(tk.END, f" {r['Recipe Name']}\nIngredients: {r['Ingredients']}\nPrep Time: {r.get('Prep Time', 'N/A')}\nCook Time: {r.get('Cook Time', 'N/A')}\nSteps: {r['Steps']}\n")
            result_box.insert(tk.END, "-------------------------------------------\n\n")

    # PARTIAL MATCHES
    if partial:
        result_box.insert(tk.END, "\n Partial Matches (Missing Ingredients Shown)\n\n")
        for r, missing, score in partial:
            result_box.insert(tk.END, f" {r['Recipe Name']}\nHave: {score} items\nMissing: {', '.join(missing)}\nSteps: {r['Steps']}\n")
            result_box.insert(tk.END, "-------------------------------------------\n\n")

    if not exact and not partial:
        result_box.insert(tk.END, "No recipe matches your ingredients!")

    result_box.configure(state='disabled')


def random_recipe():
    if len(df) == 0:
        messagebox.showinfo("Error", "No recipes found!")
        return

    row = df.sample(1).iloc[0]
    messagebox.showinfo("Surprise Recipe",
                        f"{row['Recipe Name']}\n\nIngredients: {row['Ingredients']}\n\nSteps:\n{row['Steps']}")


def add_to_favorites():
    selected = entry_fav.get().strip()
    if selected:
        save_favorite(selected)
        messagebox.showinfo("Saved", "Recipe added to favorites!")
    else:
        messagebox.showwarning("Empty", "Enter a recipe name first.")


def view_favorites():
    favs = load_favorites()
    if not favs:
        messagebox.showinfo("Favorites", "You have no favorite recipes yet.")
        return

    messagebox.showinfo("Your Favorites", "\n".join(favs))


# ---------------- GUI DESIGN ----------------
root = tk.Tk()
root.title("Recipe Finder – AI Assistant")
root.geometry("780x800")
root.config(bg="#f5efff")  # soft lilac background

title = tk.Label(root, text=" Recipe Recommendation Agent ",
                 font=("Helvetica", 20, "bold"),
                 fg="#5a189a", bg="#f5efff")
title.pack(pady=15)

lbl = tk.Label(root, text="Enter Ingredients (comma separated):",
               font=("Arial", 13, "bold"),
               fg="#7b2cbf", bg="#f5efff")
lbl.pack()

entry = tk.Entry(root, width=60, font=("Arial", 12), bg="white", fg="black", highlightthickness=2, highlightbackground="#9d4edd")
entry.pack(pady=8)

btn = tk.Button(root, text="Find Recipes",
                font=("Arial", 12, "bold"),
                bg="#9d4edd", fg="white",
                activebackground="#7b2cbf",
                relief="ridge", command=search_recipes)
btn.pack(pady=10)

surprise_btn = tk.Button(root, text="Surprise Me!",
                         font=("Arial", 12, "bold"),
                         bg="#ffb703", fg="black",
                         activebackground="#fb8500",
                         relief="ridge", command=random_recipe)
surprise_btn.pack(pady=5)

# Result Box
result_box = scrolledtext.ScrolledText(root, width=90, height=18, font=("Arial", 11), bg="#ffffff", fg="#4a4a4a")
result_box.pack(pady=12)
result_box.configure(state='disabled')

# Favorite Section
fav_label = tk.Label(root, text="Add to Favorites (enter recipe name):",
                     font=("Arial", 12), fg="#5a189a", bg="#f5efff")
fav_label.pack()

entry_fav = tk.Entry(root, width=40)
entry_fav.pack(pady=4)

fav_btn = tk.Button(root, text="Save Favorite",
                    bg="#c77dff", fg="white",
                    font=("Arial", 11, "bold"), command=add_to_favorites)
fav_btn.pack(pady=3)

view_fav_btn = tk.Button(root, text="View Favorites",
                         bg="#e0aaff", fg="black",
                         font=("Arial", 11, "bold"), command=view_favorites)
view_fav_btn.pack(pady=5)

root.mainloop()