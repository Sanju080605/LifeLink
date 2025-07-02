from pymongo import MongoClient
from tabulate import tabulate

class Donor:
    def __init__(self, name, age, blood_group, height, weight, contact):
        self.name = name
        self.age = age
        self.blood_group = blood_group
        self.height = float(height) / 100 if float(height) > 10 else float(height)  # Convert cm to meters if needed
        self.weight = float(weight)
        self.contact = contact
        self.bmi = self.calculate_bmi()

    def calculate_bmi(self):
        """Calculate BMI using weight and height."""
        return round(self.weight / (self.height ** 2), 2)

class BloodBank:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["BloodBank"]
        self.collection = self.db["Bloodbank"]
    
    def add_donor(self, donor):
        if donor.bmi >= 20:
            donor_data = {
                "name": donor.name,
                "age": donor.age,
                "blood_group": donor.blood_group,
                "height": donor.height,
                "weight": donor.weight,
                "bmi": donor.bmi,
                "contact": donor.contact
            }
            self.collection.insert_one(donor_data)
            print(f"\n✅ Donor {donor.name} added successfully to the database. BMI: {donor.bmi} (Eligible)")
        else:
            print(f"\n❌ Donor {donor.name} is NOT eligible to donate. BMI: {donor.bmi} (Below 20)")

    def find_donor(self, blood_group):
        found_donors = self.collection.find({"blood_group": blood_group})
        donors_list = list(found_donors)
        
        if donors_list:
            print(f"\nAvailable donors with blood group {blood_group}:")
            headers = ["Name", "Age", "Blood Group", "Height", "Weight", "BMI", "Contact"]
            table_data = [[d["name"], d["age"], d["blood_group"], d["height"], d["weight"], d["bmi"], d["contact"]] for d in donors_list]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        else:
            print(f"\nNo donors found with blood group {blood_group}. Please check back later.")
    
    def display_all_donors(self):
        donors = self.collection.find()
        donors_list = list(donors)
        
        if donors_list:
            print("\nAll Donors:")
            headers = ["Name", "Age", "Blood Group", "Height", "Weight", "BMI", "Contact"]
            table_data = [[d["name"], d["age"], d["blood_group"], d["height"], d["weight"], d["bmi"], d["contact"]] for d in donors_list]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No donors available.")

def main():
    blood_bank = BloodBank()

    while True:
        print("\nWelcome to the Blood Bank Management System")
        print("1. I am a Donor")
        print("2. I am a Receiver")
        print("3. Display All Donors")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':  # Donor
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            blood_group = input("Enter your blood group: ")
            height = float(input("Enter your height in cm: "))
            weight = float(input("Enter your weight in kg: "))
            contact = input("Enter your contact number: ")
            
            donor = Donor(name, age, blood_group, height, weight, contact)
            blood_bank.add_donor(donor)

        elif choice == '2':  # Receiver
            blood_group = input("Enter the blood group you need: ")
            blood_bank.find_donor(blood_group)

        elif choice == '3':  # Display all donors
            blood_bank.display_all_donors()

        elif choice == '4':  # Exit
            print("Thank you for using the Blood Bank System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
