#=====importing libraries===========
import time
from datetime import datetime

# Functions
def log_in(username, password):
    # Count how many attempts there has been
    attempts = 0
    success = False
    # While there has been less than 5 attempts, check if credentials match database
    while attempts < 5 and not success:
        with open ("user.txt", "r") as f:
            for line in f:
                u, p = line.strip().split(", ")
                if username == u and password == p:
                    print ("\nLogin successuful\n")
                    success = True
                    break

            else:
                # Add 1 to atttempts after every unsuccessful attempt
                print("Login unsucessful try again")
                attempts += 1
    # Sleep for 5 mins if attempts equals 5
    if attempts == 5:
        print ("Too many attempts Try again in 5 mins")
        time.sleep(300)

def reg_user(new_username, new_password, password_con) :

# Validation checks
    if not any (c.isdigit() for c in new_password):
        print ("Password must include at least one number and be 8 characters long")
    elif len(new_username) < 8:
        print ("Username must be at least 8 characters long")
    elif len(new_password) < 8:
         print("Password must be at least 8 characters long and contain at least one number")
    elif new_password != password_con:
        print("Passwords do not match")
    else:

    # Read lines of user.txt, if new_username is already in user.txt print error
        try:
            with open ("user.txt", "r") as login:
                for line in login:
                    u, p = line.strip().split(", ")
                    if u == new_username:
                        print ("Username already taken. Please try again\n")
                        continue
        except FileNotFoundError:
            pass

        with open ("user.txt", "a+") as login:
            login.write(f"\n{new_username}, {new_password}")
            print ("Details Added")
            
def add_task():
    task_title = input ("What is the task title?: ")
    task_for = input ("Who is the task to be assigned to?: ").lower()
    assign_date = input("Enter date assigned: ")
    Due_date = input("Enter due date: ")
    complete = input("Is the task complete?: ")
    description = input("Enter task description: ")

    with open ("tasks.txt", "a") as tasks:
        tasks.write(f"\n{task_for}, {task_title}, {description}, {assign_date}, {Due_date}, {complete}")

def view_all():
    # prints tasks in an easy to read format
    with open ("tasks.txt", "r") as tasks:
        
        for line in tasks:
            line = line.split(", ")
            print (f"Task: {line[1]}\nAssigned to: {line[0]}\nDate assigned: {line[3]}\nDue date: {line[4]}\nTask Complete?: {line[5]}\nTask description: {line[2]}\n")

def view_mine(username): 
    # An empty list to store all tasks
    all_tasks = []
    with open ("tasks.txt", "r") as tasks:
        # A counter variable to number tasks
        task_number = 1
        # A list to store the user that is logged in tasks
        my_tasks = []
        for line in tasks:
            line = line.split(", ")
            all_tasks.append(line)
            # If the first word in the line is the users name add that task to my_tasks
            if line[0] == username:
                my_tasks.append(line)
  
        while True:
            selection = int(input("""Enter '0' to view all tasks
Enter number of task to view specific task
enter '-1' to return to menu 

: """))

            if selection == -1:
                return

            elif selection == 0:
                for i, line in enumerate(my_tasks, start=1):

                    print (f"""
                    Task {i}: {line[1]}
                    Assigned to: {line[0]}
                    Date assigned: {line[3]}
                    Due date: {line[4]}
                    Task Complete?: {line[5]}
                    Task description: {line[2]}
""")
            # This section is for selecting a specific task. A valid selection must be equal or greater than 1 and less than the amount of tasks
            elif selection >= 1 and selection <= len(my_tasks): 
                
                line = my_tasks[selection - 1]

                # Removes the newline character
                line[-1] = line[-1].rstrip("\n")

                print (f"""
                    Task {selection}: {line[1]}
                    Assigned to: {line[0]}
                    Date assigned: {line[3]}
                    Due date: {line[4]}
                    Task Complete?: {line[5]}
                    Task description: {line[2]}
                    """)    
                
                # If task is not complete, ask user to edit task or mark as complete
                if line[5] == 'No':
                    
                    edit = input("""Enter 'E' to edit task
Enter 'M' to mark task as complete

:
""").lower()

                    if edit == "e":
                        
                        # Display edit options and request selection
                        edit_options = input("""Enter 'U' to change who the task is assigned to
Enter 'D' to change the due date : """).lower()

                        if edit_options == "u":
                           
                            # Change username
                            old_username = line[0]
                            edited_username = input("Enter new username : ")
                            if len(edited_username) < 8:
                                print ("Username must be at least 8 charcaters")
                            else:
                                update_username(old_username, edited_username)
                                
                        else:
                            # Change Due Date
                            if edit_options == "d":
                                old_due_date = line[4]
                                new_due_date = input( "Enter new Due Date : ")

                                update_due_date(old_due_date, new_due_date)            
                    else:
                        # Mark task as complete
                        if edit == "m":
                            mark_complete(my_tasks, all_tasks)

                print("\n")

            else:
                print ("Invalid selection")

def update_username(old_username, edited_username):
    
    lines = []
    with open ("user.txt", "r+") as login:
        
        # read user.txt and add contntes to list
        lines += login.readlines()
          
    with open ("user.txt", "w+") as login:

        # Iterate through the list and replace the old username
        for i, line in enumerate(lines):
            u, p = line.strip().split(", ")
            if u == old_username:
                password = p
                lines[i] = (f"{edited_username}, {password}\n")
     
        login.writelines(lines)

        # This part replaces the old username in the task file
        task_lines = []
        with open ("tasks.txt", "r+") as tasks:
            
            task_lines += tasks.readlines()

        with open ("tasks.txt", "w+") as tasks:
            for i, line in enumerate(task_lines):
                a, b, c, d, e, f = line.strip().split(", ")
                if a == old_username:
                    title = b
                    desc = c
                    assigned = d
                    due = e
                    complete = f

                    task_lines[i] = (f"{edited_username}, {title}, {desc}, {assigned}, {due}, {complete}\n")

            tasks.writelines(task_lines)

def update_due_date(old_due_date, new_due_date):
    
    lines = []
    with open ("tasks.txt", "r+") as tasks:
        
        # Read task file and add to a list
        lines += tasks.readlines()

    with open ("tasks.txt", "w+") as tasks:
        
        # Iterate through task file and replace old due date with new due date
        for i, line in enumerate(lines):
            a, b, c, d, e, f = line.strip().split(", ")
            if e == old_due_date:
                username = a
                title = b
                desc = c
                assigned = d
                complete = f

        lines[i] = (f"{username}, {title}, {desc}, {assigned}, {new_due_date}, {complete}\n")

        tasks.writelines(lines)

def mark_complete(my_tasks, all_tasks): 

    
    for i, line in enumerate(my_tasks, start=1):
        if line[5] == "Yes":
            print("")
        else:
            if line[5] == "No":
                
        # Display the title of the users tasks
                print(f"\n{i}: {line[1]}\n")


    task_num = int(input("Enter the number of the task to confirm you want to mark as complete : "))

    if task_num >= 1 and task_num <= len(my_tasks):

        # Create a variable to store selected task
        chosen_task = my_tasks[task_num - 1] 

        # Change the 5th element to Yes
        chosen_task[5] = "Yes" 

        # Change the chosen task in the list of all tasks to the updated versiom
        all_tasks[all_tasks.index(chosen_task)] = chosen_task

        # Remove the new line characters
        all_tasks_no_newline = [[item if i != 5 else item.strip() for i, item in enumerate(inner_list)] for inner_list in all_tasks]

        with open ("tasks.txt","w") as tasks:

        # Write the contents of all_tasks to the file
            for line in all_tasks_no_newline:
                tasks.write(f"{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]}\n")
                            
        print ("\nCompletion status updated\n")
    else:
        print ("\nInvalid Task Number\n")

def view_stats():

    with open ("tasks.txt", "r") as tasks:
       
        # Count how many tasks there is 
        task_line = tasks.readlines()
        line_count = len(task_line)
       
        with open ("user.txt", "r") as users:
           
            # Count how many users there is 
            user_line = users.readlines()
            user_line_count = len(user_line)

        print (f"Amount of tasks: {line_count}\nAmount of users: {user_line_count}")

def gen_reports():

    # Counters
    completed = 0
    not_complete = 0
    overdue = 0
    
    with open ("tasks.txt","r") as tasks:

        # Write contents of tasks file to list, Count lines
        task_line = tasks.readlines()
        line_count = len(task_line)

        # Create a variable for the current date
        today_date = datetime.now()

        for i, task in enumerate(task_line):

            # Count complete and incomplete tasks and increment corresponding counters accordingly
            a, b, c, d, e, f = task.strip().split(", ")
            if f == "Yes":
                completed += 1
            else:
                if f == "No":
                    not_complete += 1

                    # Count overdue tasks
                    due_date = datetime.strptime(e, "%d %b %Y")
                    
                    # Increment overdue counter by 1 if task if overdue
                    if today_date > due_date:
                        overdue += 1

        
        # Calculate percentage incomplete
        percentage_not = round(not_complete/line_count*100, 2)

        # Calculate percentage overdue
        percent_overdue = round(overdue/line_count*100, 2)

        
        # Write to task_overview file
    with open("task_overview.txt", "w+") as overview:
        overview.write(f"""Amount of tasks genrated and tracked : {line_count}

Amount completed : {completed}

Amount incomplete : {not_complete}

Amount incomplete and overdue : {overdue}

Percentage incomplete : % {percentage_not}

Percentage overdue : % {percent_overdue}

""")

# ---User overview---

    # List to store usernames
    usernames = []


    with open("user.txt", "r") as users_txt:

        for line in users_txt:

            # The first word of each line us users.txt is the username
            username = line.split(", ")[0]
            
            # Add usernames to username list
            usernames.append(username)

            # Count the amount of users
            user_amount = len(usernames)
    

    # List to store the username associated with each task. (If a user has 3 tasks thir name wil appear 3 times)
    task_users = []
    
    with open ("tasks.txt", "r") as tasks:

        for line in tasks:
            
            # Add the username from each task to the list
            user = line.split(", ")[0]
            task_users.append(user)



    # A dictionary to store the usernames as keys and the amount of tasks they have as values
    amount_of_tasks = {}
    
    # Iterate through task_users
    for user in task_users:

        # If the user already has a key assigned for them in the dict, increment their value by 1 for every time their username appears in task_users
        if user in amount_of_tasks:

            amount_of_tasks[user] += 1
        
        else:
             # If they dont have a key create one with a value of 1
            amount_of_tasks[user] = 1



    # A string variable to add how many tasks the user has
    user_task_counts = ""

   # A string variable to add the percentage of total tasks the users have
    user_percentages = ""


    # Calculate the total amount of tasks so i can work out percentages
    total_tasks = sum(amount_of_tasks.values())


    # Calculate percentages of total tasks assigned to each user
    for username, user_tasks in amount_of_tasks.items():
        percentage = round(user_tasks / total_tasks * 100, 2)

        # Add to string variable
        user_percentages += (f"{username} has : % {percentage} of the tasks\n\n")

        

    # calculate how many tasks each user has and add to the string variable
    for user, count in amount_of_tasks.items():

        user_task_counts += (f"{user} has : {count} tasks\n\n")

 
    # dictionarys to store amount of complete and incomplete tasks for each user
    completed_tasks_for_users = {}
    incomplete_tasks_for_users = {}
    
    # String variables to add percentage of their tasks a user have completed or not comppleted
    task_comp_perc = ""
    task_incomp_perc = ""
 


    with open("tasks.txt", "r") as tasks:
        for line in tasks:
            # 'a' represents username in tasks.txt and 'f' represents the completion status
            a, b, c, d, e, f = line.strip().split(", ")
            
            # If task is complete
            if f == "Yes":

                # If user already inn dictionary increment the value by 1
                if a in completed_tasks_for_users:
                
                    completed_tasks_for_users[a] += 1

                else:
                    # if the user is not in the dictionary add them to it with a value of 1
                    completed_tasks_for_users[a] = 1
            else:
              
              # If the task is not complete, add to the dictionary for incomplete tasks
                if f == "No":

                    if a in incomplete_tasks_for_users:

                        incomplete_tasks_for_users[a] += 1

                    else:

                        if a not in incomplete_tasks_for_users:

                            incomplete_tasks_for_users[a] = 1


    # Iterate through the dictionary that stores the amounts of completed tasks as values                    
    for username, completed in completed_tasks_for_users.items():
          
          # Calculate Percentage
        perncentage_of_users_tasks_complete = round(completed / amount_of_tasks[username] * 100, 2)
                  
             # Add to the variable created above     
        task_comp_perc += (f"{username} has completed : % {perncentage_of_users_tasks_complete} of their tasks\n\n")


    # Iterate through dictionary for incomplete tasks
    for username, incomplete in incomplete_tasks_for_users.items():

        # Calculate percentage
        percentage_of_users_tasks_incomplete = round(incomplete / amount_of_tasks[username] * 100, 2)

        task_incomp_perc += (f"{username} needs to complete : % {percentage_of_users_tasks_incomplete} of their tasks\n\n")


    # A dictionary that store the amount of overdue tasks as values for each user
    overdue_task_per_user = {}
    
    with open("tasks.txt", "r") as tasks:

       # Iterate through task file
        for line in tasks:

            # Unpack line into separate variables representing each part of the tasks
            a, b, c, d, e, f = line.strip().split(", ")
            
            e = due_date

            # If task not complete and todays date is later than due_date
            if f == "No" and today_date > e:

               # if user is already a key in the dictionary
                if a in overdue_task_per_user:

                    # Increment their value by 1
                    overdue_task_per_user[a] += 1
                else:

                    # If user is not in dictionary add them to it with a value of 1
                    overdue_task_per_user[a] = 1

    # A dictionary to stor the percentage of tasks assigned to each user that are overdue
    overdue_task_percentage = {}
    
    # A string variable to add to file later on
    overd = ""

    
    for username, overdue_tasks in overdue_task_per_user.items():
        
        # The total number of tasks for each user is looked up in the amount_of_tasks dict using name as key
        total_tasks = amount_of_tasks[username]
        
        # Calculate percentage of tasks are overdue for each user
        percentage = round(overdue_tasks / total_tasks * 100 , 2)
        
        # Assign key values for each user
        overdue_task_percentage[username] = percentage

    # Add to the string variable
    for username, percentage in overdue_task_percentage.items():
        
        overd += (f"% {percentage} of {username}'s tasks are overdue\n\n")


       # Writing to user_overview 
    with open("user_overview.txt", "w+") as user_overview:
        
        user_overview.write (f"""Users Registered : {user_amount} 

Amount of tasks generated and tracked : {line_count}


{user_task_counts}
{user_percentages}
{task_comp_perc}
{task_incomp_perc}
{overd}
        """)

def goodbye():
    print("Goodbye!!!")
    exit()


#====Login Section====
username = input("Enter Username: ").lower()
password = input("Enter Password: ")

log_in(username, password)

# Menu section
while True:
    if username == "admin":
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
s - View statistics
gr - Generate Reports
e - Exit

: ''').lower()
    
    else:
        if username != "admin":
            menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit

: ''').lower()

    if menu == "r":
        if username != "admin":
            print ("Only admin has permision to register new users")
        else:
            new_username = input ("Enter username: ").lower()
            new_password = input ("Enter password: ")
            password_con = input ("Confirm password: ")
            print("\n")   
            reg_user(new_username, new_password, password_con)
             
    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine(username)
 
    elif menu == "s":
        # This section shows statititcs to only the admin
        if username != "admin":
            print ("Only admin has permission to view statistics")
        else:
            view_stats()
            rports = input("Do you want to view reports? (yes/no) :  ").lower()
            if rports == "yes":
                gen_reports()

                contents = ""

                with open("task_overview.txt", "r") as tasks:
                    for line in tasks:
                        contents += line
                        print("\n")

                user_contents = ""        

                with open("user_overview.txt", "r") as user_overview:
                    for line in user_overview:
                        user_contents += line
                        print("\n")

                print (contents)
                print(user_contents)

    elif menu == "gr":
        gen_reports()

    elif menu == "e":
        goodbye()

    else:
        print("You have made a wrong choice, Please Try again")