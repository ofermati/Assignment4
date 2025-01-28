from persistence import repo, Activitie

import sys

def main(args: list[str]):
    inputfilename: str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline: list[str] = line.strip().split(", ")
            
            # Extract fields from the action line
            product_id = int(splittedline[0])
            quantity = int(splittedline[1])
            activator_id = int(splittedline[2])
            date = splittedline[3]

            # Find the product in the database
            product = repo.products.find(id=product_id)
            if not product or len(product) == 0:
                continue  # Skip if product does not exist

            product = product[0]

            # Handle sale action
            if quantity < 0 and product.quantity < abs(quantity):
                continue  # Skip if not enough stock

            # Calculate new quantity
            new_quantity = product.quantity + quantity
            #if new_quantity < 0:
            #    continue  # Skip if resulting quantity is invalid

            # Update the product's quantity
            repo.products.delete(id=product_id)
            repo.products.insert(product.__class__(product.id, product.description, product.price, new_quantity))

            # Log the action in the activities table
            activity = Activitie(product_id, quantity, activator_id, date)
            repo.activities.insert(activity)

if __name__ == '__main__':
    main(sys.argv)
