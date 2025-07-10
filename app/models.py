from pydantic import BaseModel
from typing import List
import uuid

class Task(BaseModel):
    id: str
    title: str
    completed: bool = False
    
    @classmethod
    def create(cls, title: str) -> 'Task':
        return cls(id=str(uuid.uuid4()), title=title)

class TodoList(BaseModel):
    tasks: List[Task] = []
    
    def add_task(self, title: str) -> Task:
        task = Task.create(title)
        self.tasks.append(task)
        return task
    
    def toggle_task(self, task_id: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                break
    
    def delete_task(self, task_id: str) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]
    
    def get_active_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        return [task for task in self.tasks if task.completed]