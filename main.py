

from scrape_fill import ScrapeFill

# calling the class
task = ScrapeFill()

# calling the scrape website method to get necessary data
task.scrape_website()

# getting the required attributes
addresses = task.address
prices = task.price
links = task.link

for num in range(0, len(addresses)):
    task.fill_form(address=addresses[num], price=prices[num], link=links[num])
