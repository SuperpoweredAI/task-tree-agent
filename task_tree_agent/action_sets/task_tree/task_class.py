class Task:
    def __init__(self, description, complete=False, parent=None):
        self.description = description
        self.complete = complete
        self.subtasks = []
        self.parent = parent

    def add_subtask(self, subtask):
        subtask.parent = self
        self.subtasks.append(subtask)

    def find_next_task(self):
        if not self.complete and (not self.subtasks or all([subtask.complete for subtask in self.subtasks])):
            return self

        for subtask in self.subtasks:
            next_task = subtask.find_next_task()
            if next_task:
                return next_task
        return None

    def print_tree(self, level=0):
        indent = "  " * level
        status = "✓" if self.complete else "✗"
        print(f"{indent}{status} {self.description}")

        for subtask in self.subtasks:
            subtask.print_tree(level + 1)

    def get_local_task_tree(self):
        local_task_tree_str = ""

        # get the parent task description
        if self.parent:
            local_task_tree_str += f"Parent Task: {self.parent.description}\n\n"

        # get the current task and sibling task descriptions
        if self.parent:
            local_task_tree_str += "Current and sibling tasks:\n"
            for i,task in enumerate(self.parent.subtasks):
                if task == self:
                    local_task_tree_str += f"  - Task {i+1}: {task.description} (CURRENT TASK)\n"
                else:
                    local_task_tree_str += f"  - Task {i+1}: {task.description}\n"
        else:
            local_task_tree_str += f"Current Task: {self.description}\n"

        return local_task_tree_str

"""
# Example usage
task_tree = Task("Write a short story.")
task_tree.add_subtask(Task("Write a title."))
task_tree.subtasks[0].add_subtask(Task("Do some brainstorming."))

# Add a sibling task
new_sibling_task = Task("Write a sentence.")
task_tree.subtasks[0].add_subtask(new_sibling_task)

# Print the whole task tree
task_tree.print_tree()

# Find the next task
next_task = task_tree.find_next_task()
print(f"\nNext task:\n{next_task}\n")

# Edit the local task tree
# Access the parent task directly using the 'parent' attribute
parent_task = next_task.parent
print(f"Parent task:\n{parent_task}\n")

# Now, edit the parent task (e.g., change its description)
parent_task.description = "Write an amazing title."
print("Task tree after editing the local task tree:")
task_tree.print_tree()

# Print the local task tree
print(f"\nLocal task tree:\n{next_task.get_local_task_tree()}")
"""