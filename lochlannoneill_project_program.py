# Author:           Lochlann O'Neill
# Student Number:   R00175741
# Class Group:      COMP1CY
# Date:             26/04/2019
# Attached Files:   reading_from_user.py, lochlannoneill_project_data.txt, lochlannoneill_project_bonus.txt

import reading_from_user
import random

def load_data(name_of_file):
    file_connection = open(name_of_file, "r")  # Opens the file in read
    employee_id_list = []  # Create empty lists to be used as destination for file content
    firstname_list = []
    surname_list = []
    email_list = []
    salary_list = []
    while True:
        line = file_connection.readline()  # Variable used for each iteration
        if line == "":
            break  # End of the file has been reached, stop reading lines
        line_data = line.split(',')  # Splits line into different pieces of data (eg. index 0 = id)
        employee_id_list.append(line_data[0])
        firstname_list.append(line_data[1])
        surname_list.append(line_data[2])
        email_list.append(line_data[3])
        salary_list.append(float(line_data[4]))  # Also convert each string to a float instead
    return employee_id_list, firstname_list, surname_list, salary_list, email_list

def show_menu(employee_id_list, firstname_list, surname_list, salary_list, email_list):
    while True:
        choice = reading_from_user.read_range_integer("\nEnter command\n\t1. View all employees\n\t"
            "2. View a particular employee\n\t3. Edit the salary of an employee\n\t"
            "4. Add a new employee\n\t5. Delete an employee\n\t"
            "6. Give a bonus to each employee, writing details to the file\n\t7. Generate a report for management\n\t"
            "8. Quit and apply all updates\n\t>>> ", 1, 8)  # minrange set to 1, maxrange set to 8
        if choice == 1:
            show_all_employees(employee_id_list, firstname_list, surname_list, salary_list, email_list)
        elif choice == 2:
            show_employee("\nEnter ID of desired employee >>> ", employee_id_list, firstname_list,
                          surname_list, salary_list, email_list)
        elif choice == 3:
            change_salary("\nEnter ID of desired employee >>> ", employee_id_list, firstname_list,
                          surname_list, salary_list)
        elif choice == 4:
            add_employee(employee_id_list, firstname_list, surname_list, salary_list, email_list)
        elif choice == 5:
            remove_employee("\nEnter ID of desired employee >>> ", employee_id_list, firstname_list, surname_list,
                            salary_list, email_list)
        elif choice == 6:
            save_bonus_info(employee_id_list, firstname_list, surname_list, salary_list)
        elif choice == 7:
            generate_report(firstname_list, surname_list, salary_list)
        elif choice == 8:  # User has to exit from menu to apply any updates which may have been made
            print("\nExited from menu\n")
            break

def show_all_employees(employee_id_list, firstname_list, surname_list, salary_list, email_list):
    print("\nThe following is a list of all current employees and their details respectively:")
    print("\t{:<16s}".format("IDs:"), end="")
    print(*employee_id_list, sep=', ')  # * symbol unpacks the list and return every element in the list
    print("\t{:<16s}".format("First Names:"), end="")
    print(*firstname_list, sep=', ')
    print("\t{:<16s}".format("Surnames:"), end="")
    print(*surname_list, sep=', ')
    print("\t{:<16s}".format("Salaries in €:"), end="")
    print(*salary_list, sep=', ')
    print("\t{:<16s}".format("Emails:"), end="")
    print(*email_list, sep=', ')

def show_employee(prompt, employee_id_list, firstname_list, surname_list, salary_list, email_list):
    user_input = reading_from_user.read_nonempty_string(prompt)
    found_index = find_employee_pos_in_list(user_input, employee_id_list)
    if found_index == -1:  # Returned from find_employee_pos_in_list() if user_input was not in the list of employee ids
        print("The employee with an ID of '{}' cannot be found".format(user_input))
    else:
        print("\t{:<16s}{:<}".format("ID: ", employee_id_list[found_index]))
        print("\t{:<16s}{:<}".format("First Name:", firstname_list[found_index]))
        print("\t{:<16s}{:<}".format("Surname:", surname_list[found_index]))
        print("\t{:<16s}{:<}".format("Email:", email_list[found_index]))
        print("\t{:<16s}€{:<.2f}".format("Salary:", salary_list[found_index]))

def change_salary(prompt, employee_id_list, firstname_list, surname_list, salary_list):
    user_input = reading_from_user.read_nonempty_string(prompt)
    found_index = find_employee_pos_in_list(user_input, employee_id_list)
    if found_index == -1:  # Returned from find_employee_pos_in_list() if user_input was not in the list of employee ids
        print("The employee with an ID of '{}' cannot be found".format(user_input))
    else:
        print("{} {} has a salary of €{}".format(firstname_list[found_index], surname_list[found_index],
                                                salary_list[found_index]))
        salary_list[found_index] = reading_from_user.read_nonnegative_float("Enter desired new salary >>> ")
        print("{}'s Salary has been changed to €{}".format(firstname_list[found_index], salary_list[found_index]))

def add_employee(employee_id_list, firstname_list, surname_list, salary_list, email_list):
    id = generate_unique_id(employee_id_list)  # Must be unique
    fname = reading_from_user.read_nonempty_alphabetical_string("\nEnter the first name of the new employee >>> ")
    lname = reading_from_user.read_nonempty_alphabetical_string("Enter the last name of the new employee >>> ")
    salary = reading_from_user.read_nonnegative_float("Enter the salary of the new employee >>> ")
    email = generate_unique_email(fname, lname, email_list)  # Must be unique
    employee_id_list.append(id)  # Add data from each list to new line in data file
    firstname_list.append(fname)
    surname_list.append(lname)
    salary_list.append(salary)
    email_list.append(email)
    print("{} {} has been given an ID of {} and has been added to current employees".format(fname, lname, id))

def remove_employee(prompt, employee_id_list, firstname_list, surname_list, salary_list, email_list):
    user_input = reading_from_user.read_nonempty_string(prompt)
    found_index = find_employee_pos_in_list(user_input, employee_id_list)
    if found_index == -1:  # Returned from find_employee_pos_in_list() if user_input was not in the list of employee ids
        print("The employee with an ID of '{}' cannot be found".format(user_input))
    else:
        print("{} {} will now be removed".format(firstname_list[found_index], surname_list[found_index]))
        del employee_id_list[found_index]
        del firstname_list[found_index]
        del surname_list[found_index]
        del salary_list[found_index]
        del email_list[found_index]

def save_bonus_info(employee_id_list, firstname_list, surname_list, salary_list):
    with open("lochlannoneill_project_bonus.txt", "w") as output:  # Opens the file as write
        print()
        for i in range(len(employee_id_list)):
            user_input = reading_from_user.read_nonnegative_float("Enter bonus percentage for employee with ID {} >>> "
                                                              .format(employee_id_list[i]))  # Prompt for every employee
            bonus_total = salary_list[i] * (user_input / 100)  # Calculate bonuses employee receives based on user input
            print(employee_id_list[i], firstname_list[i], surname_list[i],
                  user_input, "{:.2f}".format(bonus_total), sep=",", file=output)  # Save acquired data to bonus file

def generate_report(firstname_list, surname_list, salary_list):
    total_salary_sum = sum(salary_list)
    average_salary = total_salary_sum / len(salary_list)  # Denominator is the length of the salary list
    highest_salary = max(salary_list)
    print("\n{:<16s}€{:.2f}".format("Total Salary:", total_salary_sum))
    print("{:<16s}€{:.2f}".format("Average Salary:", average_salary))
    print("{:<16s}€{:.2f}".format("Highest Salary:", highest_salary))
    print("\nPeople with highest salary of €{:.2f}:".format(highest_salary))
    for i in range(len(salary_list)):
        if salary_list[i] == highest_salary:  # In the case of two employees with the same highest salary
            print("\t{} {}".format(firstname_list[i], surname_list[i]))

def find_employee_pos_in_list(id, id_list):  # Called in show_employee(), change_salary() and remove_employee()
    if id in id_list:
        found_index = id_list.index(id)
    else:
        found_index = -1
    return found_index

def generate_unique_id(employee_id_list):  # Called in add_employee()
    unique_id = random.randint(10000, 99999)
    while unique_id in employee_id_list:
        unique_id = random.randint(10000, 99999)
    return unique_id

def generate_unique_email(fname, lname, emails):  # Called in add_employee()
    unique_email = "{}.{}@cit.ie".format(fname.lower(), lname.lower())
    while unique_email in emails:
        unique_email = "{}.{}{}@cit.ie".format(fname.lower(), lname.lower(), random.randint(1, 999))  # fix this
    return unique_email

def save_data(employee_id_list, firstname_list, surname_list, salary_list, email_list, filename):  # Called in main()
    with open(filename, "w") as output:  # Opens the file in write
        for i in range(len(employee_id_list)):
            print(employee_id_list[i], firstname_list[i], surname_list[i], email_list[i],
                  salary_list[i], sep=",", file=output)

def main():
    filename = "lochlannoneill_project_data.txt"  # Provides details about employees
    employee_id_list, firstname_list, surname_list, salary_list, email_list = load_data(filename)  # Pass to show_menu()
    show_menu(employee_id_list, firstname_list, surname_list, salary_list, email_list)  # Prompts user for options
    save_data(employee_id_list, firstname_list, surname_list, salary_list, email_list, filename)  # Save all changes

main()