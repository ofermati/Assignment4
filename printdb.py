from persistence import repo

def print_table(table_name, rows):
    print(table_name)
    for row in rows:
        print(row)

def print_employees_report():
    print("Employees report")
    query = """
        SELECT e.name, e.salary, b.location, IFNULL(SUM(a.quantity * p.price), 0) AS total_sales_income
        FROM employees e
        JOIN branches b ON e.branche = b.id
        LEFT JOIN activities a ON e.id = a.activator_id
        LEFT JOIN products p ON a.product_id = p.id
        GROUP BY e.id
        ORDER BY e.name;
    """
    rows = repo.execute_command(query)
    for row in rows:
        print(" ".join(map(str, row)))

def print_activities_report():
    print("Activities report")
    query = """
        SELECT a.date, p.description, a.quantity,
               CASE WHEN a.quantity < 0 THEN e.name ELSE 'None' END AS seller_name,
               CASE WHEN a.quantity > 0 THEN s.name ELSE 'None' END AS supplier_name
        FROM activities a
        LEFT JOIN products p ON a.product_id = p.id
        LEFT JOIN employees e ON a.activator_id = e.id
        LEFT JOIN suppliers s ON a.activator_id = s.id
        ORDER BY a.date;
    """
    rows = repo.execute_command(query)
    for row in rows:
        print(" ".join(map(str, row)))

def main():
    # Print Activities table (ordered by date)
    print_table("Activities", repo.activities.find_all())

    # Print Branches table (ordered by id)
    print_table("Branches", repo.branches.find_all())

    # Print Employees table (ordered by id)
    print_table("Employees", repo.employees.find_all())

    # Print Products table (ordered by id)
    print_table("Products", repo.products.find_all())

    # Print Suppliers table (ordered by id)
    print_table("Suppliers", repo.suppliers.find_all())

    # Print the detailed employees report
    print_employees_report()

    # Print the detailed activities report
    print_activities_report()

if __name__ == '__main__':
    main()
