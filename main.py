import colorama
from colorama import Fore, Style
import json
import datetime
from datetime import datetime, timedelta
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
import pandas as pd

class App:
    def __init__(self) -> None:
        try:
            os.system("cls")
            print(Fore.RED + "Loading.... .... ... ... ... ...")
            colorama.init(autoreset=True)
        except Exception as error:
            print(Fore.RED + "Failed to connect with server...")
            print(Fore.RED + str(error))
            print(Fore.YELLOW + "Check your internet. Try to restart the app")
        
        self.choose()

    def load_data(self):
        try:
            with open("stocks.json", "r") as file:
                data = json.load(file)
                self.brands = list(data.keys())
                self.models = [model for brand in data.values() for model in brand.keys()]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(Fore.RED + "Error loading data: " + str(e))
            self.brands = []
            self.models = []
    
    def number_data_load(self):
        # Load numbers from MFS.json
        try:
            with open("MFS.json", "r") as file:
                data = json.load(file)
                self.numbers = list({number for brand in data.values() for number in brand.keys()})
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(Fore.RED + "Error loading data: " + str(e))
            self.numbers = []

    def choose(self):
        while True:
            print(Fore.GREEN + "1/ Search Product\n\n2/ Sales Registration\n\n3/ Purchase Registration\n\n4/ MFS\n\n5/ Warranty Check\n\n6/ Summary")
            choice = input(Fore.CYAN + "Enter your Choice : ")
            self.utility(choice)
            if choice == "3":
                self.Purchase_Registration()
            elif choice == "2":
                self.Sales_Registration()
            elif choice == "1":
                self.search()
            elif choice == "4":
                self.mfs()
            elif choice == "5":
                self.Warranty_Check()
            elif choice == "6":
                self.Summary()
    
    def Purchase_Registration(self):
        self.load_data()
        brand_completer = WordCompleter(self.brands, ignore_case=True)
        brand = prompt("Brand Name : ", completer=brand_completer).lower()
        self.utility(brand)
        print("\n")
        
        model_completer = WordCompleter(self.models, ignore_case=True)
        model = prompt("Model : ", completer=model_completer).lower()
        self.utility(model)
        print("\n")
        
        price = input("Per Unit Price : ")
        self.utility(price)
        print("\n")
        stock = input("Stock Units : ")
        self.utility(stock)
        print("\n")
        a = input(Fore.RED + "Press any key to Confirm .... ... ... ... ... .. ..... ... . ..")
        self.utility(a)
        print(Fore.CYAN + "Registering.... ... .. ..... .... .... ... .. .... ... ... ... ... ... .. ")
        
        # Store purchase history in purchase.json
        try:
            with open("purchase.json", "r") as file:
                content = file.read()
                if content:
                    purchase_data = json.loads(content)
                else:
                    purchase_data = {}
        except (FileNotFoundError, json.JSONDecodeError):
            purchase_data = {}

        if brand not in purchase_data:
            purchase_data[brand] = {}
        if model not in purchase_data[brand]:
            purchase_data[brand][model] = []

        purchase_data[brand][model].append({
            "date_time": datetime.now().strftime("%d/%m/%y %H:%M:%S"),
            "price": price,
            "stock": stock
        })

        with open("purchase.json", "w") as file:
            json.dump(purchase_data, file, indent=4)

        # Update stock information in stocks.json
        try:
            with open("stocks.json", "r") as file:
                content = file.read()
                if content:
                    stock_data = json.loads(content)
                else:
                    stock_data = {}
        except (FileNotFoundError, json.JSONDecodeError):
            stock_data = {}

        if brand not in stock_data:
            stock_data[brand] = {}
        if model not in stock_data[brand]:
            stock_data[brand][model] = {
                "price": price,
                "stock": stock
            }
        else:
            stock_data[brand][model]["price"] = price  # Update the price
            stock_data[brand][model]["stock"] = str(int(stock_data[brand][model]["stock"]) + int(stock))

        with open("stocks.json", "w") as file:
            json.dump(stock_data, file, indent=4)

        print(Fore.GREEN + "Done")
        input("")
        os.system("cls")

    def Sales_Registration(self):
        self.load_data()
        brand_completer = WordCompleter(self.brands, ignore_case=True)
        brand = prompt("Brand Name : ", completer=brand_completer).lower()
        self.utility(brand)
        print("\n")
        
        model_completer = WordCompleter(self.models, ignore_case=True)
        model = prompt("Model : ", completer=model_completer).lower()
        self.utility(model)
        print("\n")
        
        price = input("Per Unit Price : ")
        self.utility(price)
        print("\n")
        stock = input("Stock Units : ")
        self.utility(stock)
        print("\n")
        cname = input("Customer Name : ")
        self.utility(cname)
        print("\n")
        cnumber = input("Customer Number: ")
        self.utility(cnumber)
        print("\n")
        a = input(Fore.RED + "Press any key to Confirm .... ... ... ... ... .. ..... ... . ..")
        self.utility(a)
        print(Fore.CYAN + "Registering.... ... .. ..... .... .... ... .. .... ... ... ... ... ... .. ")
        
        try:
            with open("sales.json", "r") as file:
                content = file.read()
                if content:
                    data = json.loads(content)
                else:
                    data = {}
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Update data with new sales information
        if cnumber not in data:
            data[cnumber] = []
        data[cnumber].append({
            "customer_name": cname,
            "brand": brand,
            "model": model,
            "price": price,
            "stock": stock,  # Include stock data
            "date_time": datetime.now().strftime("%d/%m/%y %H:%M:%S")
        })

        # Deduct stock from stocks.json
        try:
            with open("stocks.json", "r") as file:
                content = file.read()
                if content:
                    stock_data = json.loads(content)
                else:
                    stock_data = {}
        except (FileNotFoundError, json.JSONDecodeError):
            stock_data = {}

        if brand in stock_data and model in stock_data[brand]:
            current_stock = int(stock_data[brand][model]["stock"])
            new_stock = current_stock - int(stock)
            if new_stock < 0:
                print("Error: Not enough stock available.")
                return
            stock_data[brand][model]["stock"] = str(new_stock)
        else:
            print("Error: Brand or model not found in stocks.json.")
            return

        with open("stocks.json", "w") as file:
            json.dump(stock_data, file, indent=4)
        
        # Write updated sales data back to the file
        with open("sales.json", "w") as file:
            json.dump(data, file, indent=4)
        
        print(Fore.GREEN + "\nDone")
        input("")
        os.system("cls")

    def search(self):
        self.load_data()
        brand_completer = WordCompleter(self.brands, ignore_case=True)
        brand = prompt("Brand Name : ", completer=brand_completer).lower()
        self.utility(brand)
        print("\n")
        
        model_completer = WordCompleter(self.models, ignore_case=True)
        model = prompt("Model : ", completer=model_completer).lower()
        self.utility(model)
        print("\n")
        a = input(Fore.RED + "Press any key to Confirm .... ... ... ... ... .. ..... ... . ..")
        self.utility(a)
        os.system("cls")
        print(Fore.CYAN + "Searching.... ... .. ..... .... .... ... .. .... ... ... ... ... ... .. \n")
        try:
            with open("stocks.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: stocks.json file not found or is invalid.")
            return
        if brand in data and model in data[brand]:
            price = data[brand][model]["price"]
            stock = data[brand][model]["stock"]
            print(Fore.YELLOW + f"Brand: {brand.capitalize()}\nModel: {model.capitalize()}\nPrice: {price}\nStock: {stock}")
        else:
            print("Brand or model not found in stocks.json.")
        
        print(Fore.GREEN + "\nDone")
        input("")
        os.system("cls")

    def utility(self, input_variable):
        if input_variable == ":q" or input_variable == ":exit":
            exit()
        elif input_variable == ":c" or input_variable == ":cancel":
            self.choose()
        elif input_variable == ":clear" or input_variable == ":cls" or input_variable == ":clean":
            os.system("cls")

    def mfs(self):
        os.system("cls")
        print(Fore.GREEN + "1/ bKash\n\n2/ Nagad\n\n3/ Rocket \n\n4/ Upay\n")
        selection = input(Fore.CYAN + "Enter your Choice : ")
        self.utility(selection)
        if selection == "1":
            self.bKash()
        elif selection == "2":
            self.Nagad()
        elif selection == "3":
            self.Rocket()
        elif selection == "4":
            self.Upay()
        
    def update_mfs(self, service_name):
        self.number_data_load()
        os.system("cls")
        number_completer = WordCompleter(self.numbers, ignore_case=True)
        number = prompt(f"Enter {service_name} Number : ", completer=number_completer)
        self.utility(number)
        print("\n")

        # Load existing data
        try:
            with open("MFS.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if service_name not in data:
            data[service_name] = {}
        if number not in data[service_name]:
            data[service_name][number] = {}

        # Determine today's date
        date_str = datetime.now().strftime("%d/%m/%y")

        # Check if today's date already exists for the given number
        if date_str in data[service_name][number]:
            if data[service_name][number][date_str]["starting balance"] !="":
                print(Fore.RED + "Error: Data for this date already exists. You cannot enter multiple inputs for the same date.")
                return
        try:
            print(Fore.YELLOW + f"\nDate : {data[service_name][number][date_str]}\n")
        except:
            pass
        
        starting_balance = input(Fore.CYAN + "Starting Balance : ")
        self.utility(starting_balance)
        print("\n")
        b2b_amount = input(Fore.CYAN + "Enter B2B Amount : ")
        self.utility(b2b_amount)
        print("\n")
        closing_balance = input(Fore.CYAN + "Closing Balance : ")
        self.utility(closing_balance)
        print("\n")

        # Update today's data
        data[service_name][number][date_str] = {
            "starting balance": starting_balance,
            "B2B": b2b_amount,
            "closing balance": closing_balance
        }

        # Save updated data
        with open("MFS.json", "w") as file:
            json.dump(data, file, indent=4)

        print(Fore.GREEN + "Data updated successfully!")

    def bKash(self):
        self.update_mfs("bKash")

    def Nagad(self):
        self.update_mfs("Nagad")

    def Rocket(self):
        self.update_mfs("Rocket")

    def Upay(self):
        self.update_mfs("Upay")

    def Warranty_Check(self):
        # Input customer number
        customer_number = input("Enter customer number: ")
        self.utility(customer_number)
        
        with open('sales.json', 'r') as file:
            sales_data = json.load(file)
        
        if customer_number in sales_data:
            customer_data = sales_data[customer_number]
            print(json.dumps(customer_data, indent=4))
            return customer_data
        else:
            print(Fore.RED + "Customer number not found.")
            return "Customer number not found."

    def Summary(self):
        print(Fore.CYAN + "1/MFS Summary\n\n2/Purchsae Summary\n\n3/Sales Summary\n\n4/Stocks Summary")
        choices = input(Fore.YELLOW + "Enter your Choice : " )
        if choices == "1":
            with open('MFS.json', 'r') as file:
                data = json.load(file)

            # Function to create Excel file for each brand
            def create_excel_file(brand_name, brand_data):
                # Prepare data for DataFrame
                rows = []
                for number, transactions in brand_data.items():
                    for date, details in transactions.items():
                        row = {
                            "Number": number,
                            "Date": date,
                            "Starting Balance": details["starting balance"],
                            "B2B": details["B2B"],
                            "Closing Balance": details["closing balance"]
                        }
                        rows.append(row)
                
                # Create DataFrame
                df = pd.DataFrame(rows)
                
                # Add brand name at the top
                df.loc[-1] = [brand_name, "", "", "", ""]  # Adding a row with brand name
                df.index = df.index + 1  # Shifting index
                df = df.sort_index()  # Sorting by index to place the brand name at the top
                
                # Save to Excel file
                file_name = f"{brand_name}.xlsx"
                df.to_excel(file_name, index=False)
                print(f"Created {file_name}")

            # Create Excel files for each brand
            for brand, brand_data in data.items():
                create_excel_file(brand, brand_data)

        elif choices == "2":
            with open('purchase.json', 'r') as file:
                data = json.load(file)

            # Prepare data for DataFrame
            rows = []
            for brand, models in data.items():
                for model, details in models.items():
                    for detail in details:
                        row = {
                            "Brand": brand,
                            "Model": model,
                            "Date_Time": detail["date_time"],
                            "Price": detail["price"],
                            "Stock": detail["stock"]
                        }
                        rows.append(row)

            # Create DataFrame
            df = pd.DataFrame(rows)

            # Save to Excel file
            file_name = "purchase_data.xlsx"
            df.to_excel(file_name, index=False)
            print(f"Created {file_name}")

        elif choices == "3":
            with open('sales.json', 'r') as file:
                data = json.load(file)

            # Prepare data for DataFrame
            rows = []
            for number, transactions in data.items():
                for transaction in transactions:
                    row = {
                        "Number": number,
                        "Customer Name": transaction["customer_name"],
                        "Brand": transaction["brand"],
                        "Model": transaction["model"],
                        "Price": transaction["price"],
                        "Stock": transaction["stock"],
                        "Date_Time": transaction["date_time"]
                    }
                    rows.append(row)

            # Create DataFrame
            df = pd.DataFrame(rows)

            # Save to Excel file
            file_name = "sales_data.xlsx"
            df.to_excel(file_name, index=False)
            print(f"Created {file_name}")

        elif choices == "4":
            # Load JSON data
            with open('stocks.json', 'r') as file:
                data = json.load(file)

            # Prepare data for DataFrame
            rows = []
            for brand, models in data.items():
                for model, details in models.items():
                    row = {
                        "Brand": brand,
                        "Model": model,
                        "Price": details["price"],
                        "Stock": details["stock"]
                    }
                    rows.append(row)

            # Create DataFrame
            df = pd.DataFrame(rows)

            # Save to Excel file
            file_name = "stock_data.xlsx"
            df.to_excel(file_name, index=False)
            print(f"Created {file_name}")

if __name__ == "__main__":
    app = App()
