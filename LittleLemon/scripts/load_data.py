import csv
from LittleLemonAPI.models import MenuItem, Category
def run():
    filename = 'LittleLemonAPI/menu_items.csv'  # replace with your actual file path
    MenuItem.objects.all().delete()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        # the format is title, price, inventory, category


        for row in reader:
            cat, created = Category.objects.get_or_create(title=row[3])
            title = row[0]
            featured = row[1]
            price = row[2]
            menu_item = MenuItem(title=title, featured=featured, price=price, category=cat)
            menu_item.save()
        