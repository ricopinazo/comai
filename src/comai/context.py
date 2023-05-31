import os
import sys
from dataclasses import dataclass

shell = os.getenv("SHELL")
if not shell:
    shell = "bash"

system = None
if sys.platform == "linux":
    system = "linux"
elif sys.platform == "darwin":
    system = "mac"


@dataclass
class Context:
    system: str
    shell: str


def get_context() -> Context:
    system = None
    if sys.platform == "linux":
        system = "linux"
    elif sys.platform == "darwin":
        system = "macOS"

    shell = os.getenv("SHELL")
    if not shell:
        shell = "bash"
    shell = shell.split("/")[-1]

    return Context(system, shell)
