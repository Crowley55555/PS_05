import requests
from bs4 import BeautifulSoup

url = "https://"

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

rows = soup.find_all("tr")
data = []

for row in rows:
    cols = row.find_all("td")
    cleaned_cols = [col.text.strip() for col in cols]
    data.append(cleaned_cols)

print(data)





# data = [
#     ['100', '200', '300'],
#     ['400', '500', '600'],
#     ['110', '125', '150']
# ]
#
# numbers =[]
#
# for row in data:
#     for text in row:
#         number = int(text)
#         numbers.append(number)
#
# print(numbers)
#
# result = []
# for number in numbers:
#         if number > 190:
#             result.append(number)
# print(result)
