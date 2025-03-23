import streamlit as sl
import function
from datetime import datetime


if "todos" not in sl.session_state:
    sl.session_state["todos"] = function.get_todo("Todos.txt")


def add_todo():
    todo_local = sl.session_state["new_todo"].strip()
    if not todo_local:  # Check if the input is empty after stripping whitespace
        sl.error("To-Do cannot be empty!")
        return

    else:
        creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sl.session_state["todos"].append(f"{todo_local.title()} | Created: {creation_time}")
        function.write_todo("Todos.txt",sl.session_state["todos"])
        sl.success(f"Added {todo_local} to your To-Do list")
        sl.session_state["new_todo"] = ""


def add_completed(todo):


    completed_already = todo.count("Completed")
    if completed_already > 0:
        sl.error("This To-Do is already marked as completed.")
        return


    try:
        creation_time_str = todo.split("|")[1].strip().replace("Created: ", "")
        creation_time_obj = datetime.strptime(creation_time_str, "%Y-%m-%d %H:%M:%S")
    except (IndexError, ValueError):
        sl.error("Invalid To-Do format. Unable to extract creation time.")
        return

    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    completion_time_obj = datetime.strptime(completion_time, "%Y-%m-%d %H:%M:%S")

    duration_seconds = (completion_time_obj - creation_time_obj).total_seconds()
    duration_minutes, duration_seconds = divmod(duration_seconds, 60)
    duration_hours, duration_minutes = divmod(duration_minutes, 60)

    duration_str = f"{int(duration_hours)}h {int(duration_minutes)}m"

        # Find and update the To-Do item
    sl.session_state["todos"][sl.session_state["todos"].index(todo)] += f" | Completed: {completion_time} | Duration: {duration_str}"
    function.write_todo("Todos.txt", sl.session_state["todos"])  # Update the file with changes
    sl.session_state["todos"] = sl.session_state["todos"]  # Update session state (used for UI updates)
    sl.success(f"'{todo}' marked as completed!")
    sl.rerun()


def delete_completed():
    completed_todos = [todo for todo in sl.session_state["todos"] if "Completed" in todo]
    print(completed_todos)
    sl.session_state["todos"] = [todo for todo in sl.session_state["todos"] if "Completed" not in todo]
    function.write_todo("Todos.txt", sl.session_state["todos"])
    if completed_todos:
        sl.success(f"Deleted {len(completed_todos)} completed To-Do(s)!")
        sl.rerun()
    else:
        sl.info("No completed To-Do items to delete.")




sl.title("My Todo website")
sl.subheader("A site to check to do")
sl.write("This is a test")




for todo in sl.session_state["todos"]:
    if "Completed" in todo:
        sl.checkbox(todo, key=todo, disabled=True,value=True
)
    else:
        if sl.checkbox(todo, key=todo):
            add_completed(todo)  # Mark the To-Do as completed when checkbox is ticked

sl.text_input(label="Add a new To-Do", label_visibility="collapsed",placeholder="Enter a To-Do", on_change=add_todo, key="new_todo")

if sl.button("Delete All Completed To-Dos"):
    delete_completed()
