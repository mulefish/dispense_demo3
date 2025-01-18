import subprocess

SCRIPTS_TO_RUN = [
    "create_database.py",
    "create_tables.py",
    "populate_merchants.py",
    "populate_stores.py",
    "populate_inventory.py",
    "populate_featured_products.py",
    "populate_users.py",
    "CheckIfOK.py"
]

def run_scripts():
    for script in SCRIPTS_TO_RUN:
        try:
            print(f"Running {script} with 'uv run'...")
            #subprocess.run(["python", script], check=True)
            subprocess.run(["uv", "run", script], check=True)
            print(f"{script} completed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running {script}: {e}\n")
            break

if __name__ == "__main__":
    run_scripts()
