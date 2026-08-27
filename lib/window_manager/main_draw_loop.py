import subprocess


def clear_screen():
    _ = subprocess.run("cls||clear", shell=True, check=False)
