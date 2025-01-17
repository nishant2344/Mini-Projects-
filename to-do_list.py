from datetime import datetime

tasks = [] 
completed_tasks = []  

def addtask():
    task = input("Please enter a task: ")
    task_entry = {
        "description": task,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date_completed": None
    }
    tasks.append(task_entry)
    print(f"Task '{task}' added to the list on {task_entry['date_added']}.")

def listtasks():
    if not tasks:
        print("There are no tasks currently.")
    else:
        print("Current tasks: ")
        for index, task in enumerate(tasks):
            print(f"Task #{index}: {task['description']} (Added: {task['date_added']})")
    
    if completed_tasks:
        print("\nCompleted tasks: ")
        for index, task in enumerate(completed_tasks):
            print(f"Task #{index}: {task['description']} (Added: {task['date_added']}, Completed: {task['date_completed']})")

def deletetask():
    listtasks()
    try:
        tasktodelete = int(input("Enter the number of the task to delete: "))
        if 0 <= tasktodelete < len(tasks):
            removed_task = tasks.pop(tasktodelete)
            print(f"Task '{removed_task['description']}' has been removed.")
        else:
            print(f"Task #{tasktodelete} was not found.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

def donetasks():
    listtasks()
    try:
        task_to_mark = int(input("Enter the number of the task to mark as done: "))
        if 0 <= task_to_mark < len(tasks):
            completed_task = tasks.pop(task_to_mark)
            completed_task["date_completed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            completed_tasks.append(completed_task)
            print(f"Task '{completed_task['description']}' has been marked as done on {completed_task['date_completed']}.")
        else:
            print(f"Task #{task_to_mark} was not found.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

if __name__ == "__main__":
    print("Welcome to the *to-do* list app :)")
    while True:
        print("\n")
        print("Please select one of the following options")
        print("------------------------------------------")
        print("1. Add a new task")
        print("2. Delete a task")
        print("3. List tasks")
        print("4. Mark a task as done")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            addtask()
        elif choice == "2":
            deletetask()
        elif choice == "3":
            listtasks()
        elif choice == "4":
            donetasks()
        elif choice == "5":
            print("Goodbye!! :)")
            break
        else:
            print("Invalid input. Please try again.")
