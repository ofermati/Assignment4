from persistence import *

import sys
import os

def add_branche(splittedline : list[str]):
    branch_id, location, num_employees = splittedline #מפצל את רשימת השדות של הקלט
    branch = Branche(int(branch_id), location, int(num_employees))
    repo.branches.insert(branch)

def add_supplier(splittedline : list[str]):
    supplier_id, name, contact_information = splittedline
    supplier = Supplier(int(supplier_id), name, contact_information)
    repo.suppliers.insert(supplier)

def add_product(splittedline : list[str]):
    id, description, price, quantity = splittedline
    product = Product(int(id), description, float(price), int(quantity))
    repo.products.insert(product)


def add_employee(splittedline : list[str]):
    id, name, salary, branche = splittedline
    employee = Employee(int(id), name, float(salary), int(branche))
    repo.employees.insert(employee)

adders = {  "B": add_branche,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    inputfilename = args[1]
    # delete the database file if it exists
    repo._close()
    # uncomment if needed
    if os.path.isfile("bgumart.db"):
        os.remove("bgumart.db")
    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            adders.get(splittedline[0])(splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)