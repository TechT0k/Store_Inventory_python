

#####  PROJECT PART 2 ######


"""
Dear Students,

We have received a couple of questions, so let me try to clarify a couple of things:

a) Part 2 is essentially a re-write of the code that you did for Part 1 but in much better organized form (use classes!) and with the added feature of user input.

b) You should put the code for Part 2 into a new file named part2.py. The file will be in the same repository as when you worked on Part 1.

c) You should NOT use the output files from Part 1 as input for Part 2. The code should be independent of the output files and use the same input files as we used in part 1.

The deadline for the submission of Part2 will be extended to Sunday, November 24 at midnight.

Please reach out if you have more questions.

!!!! Change the service dates on the input file to after today. otherwise it won't return any inventory. !!!!!

9034210,5/27/2020
2390112,7/2/2020
2347800,7/3/2020
7346234,9/1/2020
1009453,10/1/2020
1167234,2/1/2021
3001265,12/1/2023

!!!! Parse through the inputfile (fullinventory) and ouput the item that fits the bill as well as an alternative if available. !!!

****************************************************************

Instructions
Improve your code design and add Interactive Inventory Query Capability

Query the user of an item by asking for manufacturer and item type.
  Print a message (“No such item in inventory”) if either the manufacturer or the item type is not in the inventory,
      more than one of either type is submitted or the combination is not in the inventory. 
      Ignore any other words, so “nice Apple computer” is treated the same as “Apple computer”.
  Print “Your item is:” with the item ID, manufacturer name, item type, and price on one line.
      Do not provide items that are past their service date or damaged. If there is more than one item, provide the most expensive item.
  Also, print “You may, also, consider:” and print information about the same item type from another manufacturer that closest in price to the output item.
      Only print this if the same item from another manufacturer is in the inventory and is not damaged nor past its service date.
  After output for one query, query the user again. Allow ‘q’ to quit.

Using Classes is MANDATORY. 
Using Pandas is Prohibited. 

Commit all your .py files on GitHub.  Use the same GitHub repo as in part 1. Provide a link on Canvas. 

Name all your files starting with “FinalProject” for example FinalProjectInput.py

Comment your code extensively. 

    #######  6 Program objectives

    1. Ask the user for MANUFACTURER and ITEM TYPE 
    2. Print a message (“No such item in inventory”) if either the manufacturer or the item type is not in the inventory, 
            more than one of either type is submitted
            combination is not in the inventory 
            ignore any other words other than MANUFACTURER and ITEM TYPE
    3. Print “Your item is:” with the item ID, manufacturer name, item type, and price on one line.
            Do not provide items that are past their service date or damaged.
            If there is more than one item, provide the most expensive item.
    4. print “You may, also, consider:” and print information about the SAME ITEM type from another manufacturer
            that is close in price to the output item
            only print if NOT DAMAGED and NOT PAST SERVICE DATE
    5. Query the user again. Allow ‘q’ to quit
    6. Use classes. 

    Input (3) files: ManufacturerList, PriceList, ServiceDatesList  
    Output: 
        "Your item is"
        "You may, also consider:"


"""

## 11/19 (5:00 - )
## 11/22 (11:00 - 11:40 - 12:00 - 12:30 - 1:00 )
     # ( - 2:30 )
## 11/23 (1:00 - )

                                                              #### CODE ####

                                                    ### CLASS DEFINITIONS AND METHODS ###


import datetime
from datetime import date



class Item:
    def __init__(self, item_data):
        self.id = item_data[0]
        self.manufacturer = item_data[1]
        self.item_type = item_data[2]
        self.price = None  # Initialize price and service dates as None
        self.service_dates = None

    def add_price(self, price):
        self.price = float(price)

    def add_service_dates(self, service_dates):
        self.service_dates = service_dates


class Inventory:
    def __init__(self, filename):
        self.data = self.read_file(filename)

    def read_file(self, filename):
        with open(filename, 'r') as file:
            list_of_lists = []
            for line in file:
                line = line.strip()
                if not line:
                    continue
                items = line.split(',')
                list_of_lists.append(items)
        return list_of_lists

    def append_items(self, new_items, item_id_index):
        for item in new_items:
            item_id = item[item_id_index]
            for existing_item in self.data:
                if existing_item[item_id_index] == item_id:
                    existing_item.extend(item[item_id_index + 1:])
                    break

    def sort_by_manufacturer(self):
        self.data = sorted(self.data, key=lambda x: x[1])  # Sort by manufacturer (index 1)
        #print(self.data)

    def get_all_manufacturers(self):
        return set(item[1] for item in self.data)
    
    def get_all_item_types(self):
        return set(item[2] for item in self.data)

    def search(self, query):
      matches = []
      query_words = query.lower().split()

      ###### (code for ignoring unwanted items in query)
      """
      

      # Handle queries with fewer than two words
      if len(query_words) < 2:
          print("Please enter at least two words (manufacturer and item type).")
          return matches

      # Identify potential manufacturer and item type indices
      manufacturer_index = 0
      item_type_index = 1

      # Check if the first word is a valid manufacturer or item type
      if query_words[0] not in self.get_all_manufacturers() and query_words[0] not in self.get_all_item_types():
        manufacturer_index = 1
        item_type_index = 2

      if item_type_index >= len(query_words):
        print("Invalid query format. Please enter a valid manufacturer and item type.")
        return matches

      # Extract manufacturer and item type from the query
      manufacturer = query_words[manufacturer_index]
      item_type = query_words[item_type_index]
        ### receiving error: IndexError: list index out of range.
        """
      #######

      for item in self.data:
        print(f"Processing item: {item}")  # debug
        if all(word in item[i].lower() for word, i in zip(query_words, [1, 2])):
            print(f"  - Query matches: {query.lower()} in {item[1].lower()} and {item[2].lower()}")  # debug
            try:
                expiry_date = datetime.datetime.strptime(item[-1], "%m/%d/%Y").date()
                print(f"  - Expiry date: {expiry_date}")  # debug
            except ValueError:
                print(f"Invalid expiry date format for item {item[0]}")
                continue

            print(f"  - Checking expiry date: {expiry_date} <= {datetime.date.today()}")  # debug
            if expiry_date <= datetime.date.today() or item[-3] == "damaged":
                print(f"  - Item is expired or damaged")  # debug
                continue
            matches.append(item)

      if not matches:
        print("No such item in inventory.")
      elif len(matches) > 1:
        print("Multiple items found. Selecting the most expensive:")
        matches = sorted(matches, key=lambda x: float(x[3]), reverse=True)
        print("Your item is:", *matches[0])

        # Find similar items from other manufacturers
        best_match = matches[0]
        similar_items = [item for item in self.data if item[2] == best_match[2] and item[1] != best_match[1] and item[-3] != 'damaged' and datetime.datetime.strptime(item[-1], "%m/%d/%Y").date() > datetime.date.today()]
        if similar_items:
            similar_items = sorted(similar_items, key=lambda x: abs(float(x[3]) - float(best_match[3])))[:3]
            print("You may also consider:")
            for item in similar_items:
                print(f"- {item[1]} {item[2]} for ${item[3]}")
      else:
        print("Your item is:", *matches[0])

        # Find similar items from other manufacturers
        best_match = matches[0]
        similar_items = [item for item in self.data if item[2] == best_match[2] and item[1] != best_match[1] and item[-3] != 'damaged' and datetime.datetime.strptime(item[-1], "%m/%d/%Y").date() > datetime.date.today()]
        if similar_items:
            similar_items = sorted(similar_items, key=lambda x: abs(float(x[3]) - float(best_match[3])))[:3]
            print("You may also consider:")
            for item in similar_items:
                print(f"- {item[1]} {item[2]} for ${item[3]}")

      return matches

        

                                                    ### MAIN FUNCTION ####

import datetime
from datetime import date

def main():
    manufacturer_list = "G:\My Drive\FALL_24\CIS_1348\PROJECT\cis1348-fa24-project-jromcodz\ManufacturerList.txt"
    price_list = "G:\My Drive\FALL_24\CIS_1348\PROJECT\cis1348-fa24-project-jromcodz\PriceList.txt"
    service_list = "G:\My Drive\FALL_24\CIS_1348\PROJECT\cis1348-fa24-project-jromcodz\ServiceDatesList.txt"

    inventory = Inventory(manufacturer_list)  # Create Inventory object for manufacturer list
    inventory.append_items(Inventory(price_list).data, 0)  # Append price data from price list using append items method
    inventory.append_items(Inventory(service_list).data, 0)  # Append service dates from service list
    inventory.sort_by_manufacturer() # Using the sort_by_manufacturer() method of the inventory class.

    query = input("Please enter Manufacturer Name and Item Type: ")
    inventory.search(query)
  
    while True:
        query = input("Please enter Manufacturer Name and Item Type (or 'q' to quit): ")
        if query.lower() == 'q':
            break
        inventory.search(query)

if __name__ == "__main__":
    main()














































































