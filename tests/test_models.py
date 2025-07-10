import pytest
from app.models import Task, TodoList

def test_task_creation():
    """Test creating a task"""
    task = Task.create('Test task')
    
    assert task.title == 'Test task'
    assert not task.completed
    assert task.id is not None
    assert isinstance(task.id, str)
    
    # Test that each task gets a unique ID
    task2 = Task.create('Another task')
    assert task.id != task2.id

def test_todo_list_operations():
    """Test TodoList operations"""
    todo_list = TodoList()
    
    # Test adding tasks
    task1 = todo_list.add_task('First task')
    task2 = todo_list.add_task('Second task')
    
    assert len(todo_list.tasks) == 2
    assert task1 in todo_list.tasks
    assert task2 in todo_list.tasks
    
    # Test toggling completion
    todo_list.toggle_task(task1.id)
    assert task1.completed
    assert not task2.completed
    
    # Test filtering tasks
    active = todo_list.get_active_tasks()
    completed = todo_list.get_completed_tasks()
    
    assert len(active) == 1
    assert len(completed) == 1
    assert active[0] == task2
    assert completed[0] == task1
    
    # Test deleting tasks
    todo_list.delete_task(task1.id)
    assert len(todo_list.tasks) == 1
    assert task1 not in todo_list.tasks
    assert task2 in todo_list.tasks

def test_todo_list_toggle_nonexistent_task():
    """Test toggling a task that doesn't exist"""
    todo_list = TodoList()
    task = todo_list.add_task('Test task')
    
    # This should not raise an error
    todo_list.toggle_task('nonexistent-id')
    
    # Original task should be unchanged
    assert not task.completed

def test_todo_list_delete_nonexistent_task():
    """Test deleting a task that doesn't exist"""
    todo_list = TodoList()
    task = todo_list.add_task('Test task')
    
    # This should not raise an error
    todo_list.delete_task('nonexistent-id')
    
    # Original task should still exist
    assert len(todo_list.tasks) == 1
    assert task in todo_list.tasks