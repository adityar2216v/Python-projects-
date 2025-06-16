import datetime

class Task:
    def __init__(self, task_id, description, due_date=None, priority="medium"):
        self.task_id = task_id
        self.description = description
        self.due_date = due_date  # datetime.date object
        self.priority = priority  # e.g., "low", "medium", "high"
        self.is_completed = False
        self.completed_date = None

    def mark_as_completed(self):
        if not self.is_completed:
            self.is_completed = True
            self.completed_date = datetime.date.today()
            print(f"Task '{self.description}' (ID: {self.task_id}) marked as completed.")
        else:
            print(f"Task '{self.description}' (ID: {self.task_id}) is already completed.")

    def __str__(self):
        status = "Completed" if self.is_completed else "Pending"
        due_info = f", Due: {self.due_date}" if self.due_date else ""
        completed_info = f", Completed: {self.completed_date}" if self.completed_date else ""
        return (f"Task ID: {self.task_id}, Description: '{self.description}', "
                f"Priority: {self.priority.capitalize()}, Status: {status}{due_info}{completed_info}")

class ToDoList:
    def __init__(self, name="My To-Do List"):
        self.name = name
        self.tasks = {}
        self._next_task_id = 1

    def add_task(self, description, due_date=None, priority="medium"):
        task_id = f"T{self._next_task_id:04d}"
        task = Task(task_id, description, due_date, priority)
        self.tasks[task_id] = task
        self._next_task_id += 1
        print(f"Task '{description}' added with ID: {task_id}.")
        return task

    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def mark_task_completed(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.mark_as_completed()
        else:
            print(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        if task_id in self.tasks:
            deleted_task = self.tasks.pop(task_id)
            print(f"Task '{deleted_task.description}' (ID: {task_id}) deleted.")
            return True
        else:
            print(f"Task with ID {task_id} not found.")
            return False

    def get_all_tasks(self):
        return list(self.tasks.values())

    def get_pending_tasks(self):
        return [task for task in self.tasks.values() if not task.is_completed]

    def get_completed_tasks(self):
        return [task for task in self.tasks.values() if task.is_completed]

    def get_tasks_by_priority(self, priority):
        return [task for task in self.tasks.values() if task.priority.lower() == priority.lower()]

    def get_overdue_tasks(self):
        today = datetime.date.today()
        return [task for task in self.tasks.values() if not task.is_completed and task.due_date and task.due_date < today]

    def __str__(self):
        return f"To-Do List: {self.name} | Total Tasks: {len(self.tasks)}"

# Example Usage:
if __name__ == "__main__":
    my_list = ToDoList("Personal Tasks")
    print(my_list)

    # Add tasks
    task1 = my_list.add_task("Buy groceries", datetime.date(2024, 7, 25), "high")
    task2 = my_list.add_task("Finish project report", datetime.date(2024, 7, 20), "high")
    task3 = my_list.add_task("Call mom", priority="medium")
    task4 = my_list.add_task("Read a book", datetime.date(2024, 7, 18), "low")

    print("\n--- All Tasks ---")
    for task in my_list.get_all_tasks():
        print(task)

    # Mark a task as completed
    print("\n--- Marking Task T0001 as Completed ---")
    my_list.mark_task_completed("T0001")
    print(my_list.get_task("T0001"))

    # Get pending tasks
    print("\n--- Pending Tasks ---")
    for task in my_list.get_pending_tasks():
        print(task)

    # Get tasks by priority
    print("\n--- High Priority Tasks ---")
    for task in my_list.get_tasks_by_priority("high"):
        print(task)

    # Simulate an overdue task (if current date is after 2024-07-18)
    print("\n--- Overdue Tasks ---")
    for task in my_list.get_overdue_tasks():
        print(task)

    # Delete a task
    print("\n--- Deleting Task T0003 ---")
    my_list.delete_task("T0003")

    print("\n--- All Tasks After Deletion ---")
    for task in my_list.get_all_tasks():
        print(task)