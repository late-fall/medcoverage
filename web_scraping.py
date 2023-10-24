from bs4 import BeautifulSoup #pip install beautifulsoup4
import requests
import re #regex

# url = "https://www.newegg.ca/msi-geforce-rtx-4070-ti-rtx-4070-ti-gaming-x-trio-12g/p/N82E16814137771?Item=N82E16814137771"

# result = requests.get(url) #will return the content of the page, and will be stored in result.
# doc = BeautifulSoup(result.text, "html.parser")

# prices = doc.find_all(text="$")
# parent = prices[0].parent
# strong = parent.find("strong")
# print(strong.string)

# print('end of lesson1')

# .find() gives first result
# .find_all() gives all resuts

# with open("index.html", "r") as f:
#     doc = BeautifulSoup(f, "html.parser")

# tag = doc.find("option")
# tag['value'] = 'new value' # changing value of attributes
# tag['color'] = "blue" # adding attribute
# print(tag.attrs) # print all attributes

# tags = doc.find_all(["p","div", "li"]) # find all with these tags
# print(tags)

# tags = doc.find_all(["option"], text="Undergradaute", value="undergraduate")
# print(tags)

# tags = doc.find_all(class_="btn-item") #find all class with btn-item, need underscore at the end. 
# print(tags)

# tags = doc.find_all(text=re.compile("\$.*"), limit=1) #find anything that comes after $ sign.
# for tag in tags:
#     print(tag.strip())

# tags = doc.find_all("input", type="text")
# for tag in tags:
#     tag['placeholder'] = "I changed it"

# with open("changed.html", "w") as file:
#     file.write(str(doc))


# with open("index.html", "r") as f:
#     doc = BeautifulSoup(f, "html.parser") 

# print(doc.prettify()) # gives you indentation, and easier to read

# tag = doc.title
# print(tag.string) # access tag title, and access string only
# tag.string = "hello" # this will modify

# print(doc) # changes title as well
# tags = doc.find_all("p") # print all with p tags
# print(tags.find_all("b")) # access all b tags inside the p tag above. 

url = "https://coinmarketcap.com/"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

tbody = doc.tbody
trs = tbody.contents #insdie of tbody
print(trs[0].next_siblings) #generator object, traversing on the same level

print(trs[0].children) #gives descendants of tag. list() to print out.

prices = {}
for tr in trs[:10]:
    name, price = tr.contents[2:4]
    fixed_name = name.p.string
    fixed_price = price.a.string

    prices[fixed_name] = fixed_price

print(prices)
