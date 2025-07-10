from nicegui import ui, app
from app.models import TodoList, Task

def create():
    @ui.page('/')
    def todo_page():
        # Initialize or get existing todo list from client storage
        if 'todo_list' not in app.storage.client:
            app.storage.client['todo_list'] = TodoList().model_dump()
        
        # Create TodoList instance from stored data
        todo_list = TodoList.model_validate(app.storage.client['todo_list'])
        
        # Main title
        ui.label('My Todo App').classes('text-4xl font-bold text-center mb-8')
        
        # Input container
        with ui.row().classes('w-full max-w-md mx-auto mb-6'):
            task_input = ui.input(
                label='Enter new task',
                placeholder='What needs to be done?'
            ).classes('flex-grow')
            
            def add_task():
                if task_input.value and task_input.value.strip():
                    todo_list.add_task(task_input.value.strip())
                    task_input.value = ''
                    # Save to storage
                    app.storage.client['todo_list'] = todo_list.model_dump()
                    update_task_list()
                    ui.notify('Task added successfully!', type='positive')
            
            ui.button(
                'Add Task',
                on_click=add_task,
                color='primary'
            ).classes('ml-2')
            
            # Allow adding task with Enter key
            task_input.on('keydown.enter', add_task)
        
        # Task list container
        task_container = ui.column().classes('w-full max-w-md mx-auto')
        
        def update_task_list():
            task_container.clear()
            
            # Show active tasks
            active_tasks = todo_list.get_active_tasks()
            completed_tasks = todo_list.get_completed_tasks()
            
            if active_tasks:
                with task_container:
                    ui.label('Active Tasks').classes('text-xl font-semibold mb-4')
                    for task in active_tasks:
                        create_task_item(task, todo_list, update_task_list)
            
            if completed_tasks:
                with task_container:
                    ui.separator().classes('my-4')
                    ui.label('Completed Tasks').classes('text-xl font-semibold mb-4')
                    for task in completed_tasks:
                        create_task_item(task, todo_list, update_task_list)
            
            if not active_tasks and not completed_tasks:
                with task_container:
                    ui.label('No tasks yet. Add one above!').classes('text-gray-500 text-center py-8')
        
        # Initial render
        update_task_list()

def create_task_item(task: Task, todo_list: TodoList, update_callback):
    """Create a single task item with checkbox and delete button"""
    
    def toggle_task():
        todo_list.toggle_task(task.id)
        # Save to storage
        app.storage.client['todo_list'] = todo_list.model_dump()
        update_callback()
    
    def delete_task():
        todo_list.delete_task(task.id)
        # Save to storage
        app.storage.client['todo_list'] = todo_list.model_dump()
        update_callback()
        ui.notify('Task deleted', type='warning')
    
    with ui.row().classes('w-full items-center p-3 border border-gray-200 rounded-lg mb-2'):
        # Checkbox
        ui.checkbox(
            value=task.completed,
            on_change=toggle_task
        ).classes('mr-3')
        
        # Task text
        text_classes = 'flex-grow text-lg'
        if task.completed:
            text_classes += ' line-through text-gray-500'
        
        ui.label(task.title).classes(text_classes)
        
        # Delete button
        ui.button(
            icon='delete',
            on_click=delete_task,
            color='negative'
        ).classes('ml-2').props('flat round')