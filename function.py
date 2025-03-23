import streamlit


def get_todo(filepath):
    with open(filepath, "r") as file_local:
        todos_local = file_local.read().splitlines()
    return todos_local


def write_todo(filepath, todos_arg):
    with open(filepath, "w") as file_local:
        file_local.writelines([todo + "\n" for todo in todos_arg])
