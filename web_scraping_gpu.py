from bs4 import BeautifulSoup
import requests
import re

user_input = input("What would you like to search for? ")

# will store the items of the user's input
item_found = {}

url = f"https://www.newegg.com/p/pl?d=3080&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

# finding the line where amount of pages is listed
page_text = doc.find(class_="list-tool-pagination-text").strong

# splitting in order to find the page number of what user is searching for
num_pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

# asking user how many pages they would like to search
page_input = input("How many pages would you like to search? There are {} total pages. ".format(num_pages))
while int(page_input) > int(num_pages) or int(page_input) < 1:
    page_input = input("There are only {} pages. Please enter another page number. ".format(num_pages))
    if int(page_input) <= int(num_pages) and int(page_input) > 0:
        break

# this will get go through the pages
for page in range(1, int(page_input) + 1):
    url = f"https://www.newegg.com/p/pl?d={user_input}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    # needs the div so that it can only look at the products
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    
    # will match the text
    hits = div.find_all(text=re.compile(user_input))

    for i in hits:
        parent = i.parent
        # need to make sure that the parent is an <a> tag so that link can be provided
        if parent.name != "a":
            continue
        link = parent["href"]
        # need to find the parent for the price
        next_parent = i.find_parent(class_="item-container")
        # using exception handling for cases where there is no strong tag
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            item_found[i] = {"Price": int(price.replace(",", "")), "Link": link}
        except:
            pass

# using lambda as an anon function using x as the items
sort_items = sorted(item_found.items(), key=lambda x: x[1]["Price"])

# getting user input to see how many results they would like to see
num_item = input("How many items would you like to see? There are {} items. ".format(len(sort_items)))
while int(num_item) > len(sort_items) or int(num_item) < 0:
    num_item = input("There are only {} items. Please enter another another number. ".format(len(sort_items)))
    if int(page_input) <= int(num_pages) and int(page_input) > 0:
        break

# printing the amount of results the user wants to see
counter = 0
for i in sort_items:
    if counter == int(num_item):
        break
    else:
        print(i[0])
        print("${}".format(i[1]["Price"]))
        print(i[1]["Link"])
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
        counter += 1
