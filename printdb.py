from persistence import *

def main():
    print("Activities:")
    for activity in repo.activities.find_all():
        print(f"{activity.date}, {activity.product_id}, {activity.quantity}, {activity.activator_id}")

    print("Branches:")
    for branch in sorted(repo.branches.find_all(), key=lambda x: x.id):
        print(f"{branch.id}, {branch.location}, {branch.number_of_employees}")

    print("Employees:")
    for employee in sorted(repo.employees.find_all(), key=lambda x: x.name):
        print(f"{employee.name}, {employee.salary}, {employee.branche}")

    print("Products:")
    for product in sorted(repo.products.find_all(), key=lambda x: x.id):
        print(f"{product.id}, {product.description}, {product.price}, {product.quantity}")

    print("Suppliers:")
    for supplier in sorted(repo.suppliers.find_all(), key=lambda x: x.id):
        print(f"{supplier.id}, {supplier.name}, {supplier.contact_information}")

    # Detailed Employee Report
    print("Employee Report:")
    employee_report = repo.execute_command(
        """
        SELECT employees.name, employees.salary, branches.location, 
               SUM(activities.quantity * products.price) as total_sales_income
        FROM employees
        JOIN branches ON employees.branche = branches.id
        LEFT JOIN activities ON employees.id = activities.activator_id
        LEFT JOIN products ON activities.product_id = products.id
        GROUP BY employees.id
        ORDER BY employees.name;
        """
    )
    for row in employee_report:
        print(" ".join(map(str, row)))

    # Detailed Activity Report
    print("Activity Report:")
    activity_report = repo.execute_command(
        """
        SELECT activities.date, products.description, activities.quantity, 
               employees.name as seller_name, suppliers.name as supplier_name
        FROM activities
        LEFT JOIN products ON activities.product_id = products.id
        LEFT JOIN employees ON activities.activator_id = employees.id
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        ORDER BY activities.date;
        """
    )
    for row in activity_report:
        print(" ".join(map(str, row)))

if __name__ == '__main__':
    main()
