# task_manager
A task management system I built during HyperionDev bootcamp

This program is designed to help a small business manage tasks for employees.


tasks.txt stores a list with details of tasks
user.txt stores usernames and passwords

The program allows people to log in, and displays a a different menu depending if the user is an admin or not
An admin has the options to :

Register a user
Add a task
View all tasks
View my tasks
View statistics
Generate reports
Exit

Regular users have less options.

When an admin registers a user some password and username rules are enforced
such as password must be at least 8 charcaters long
and username cant already be taken

When the admin selects 'Generate Reports' two text files called 'task_overview.txt' and 'user_overview' are created.

task_overview contains:

Total number of tasks generated and tracked
Total completed
Total uncomplete
Uncomplete and overdue
Percentage incomplete
Percentage overdue

user_overview contains:

Total number of tasks assigned to each user
The percentage of the total of tasks are assigned to each user
The percentage of tasks assigned to each user that are complete
The percentage of tasks assigned to each user that are not complete
The percentage of tasks assigned to each user that need to be complteted and are overdue


Users can also 
view a specific task and mark as complete
update due dates
update usernames
update who task is assigned to
...

This program is still a work in progress and I plan on improving.







