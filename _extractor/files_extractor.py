import ast
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.resolve()

SOURCE_ROOT = PROJECT_ROOT / "components"
BUILD_ROOT = PROJECT_ROOT / "build"


def get_components_dependencies(file_path):
    """
    Returns a list of components.* imports found in a Python file.
    """

    dependencies = []

    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    for node in ast.walk(tree):

        # from components.xxx import Y
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("components."):
                dependencies.append(node.module)

        # import components.xxx
        elif isinstance(node, ast.Import):
            for name in node.names:
                if name.name.startswith("components."):
                    dependencies.append(name.name)

    return dependencies

def module_to_file(module_name):
    """
    components.small.button
        ↓
    components/small/button.py
    """

    return PROJECT_ROOT / (module_name.replace(".", "/") + ".py")


def collect_dependencies(file_path, collected):
    """
    Recursive dependency collector.
    """

    file_path = Path(file_path).resolve()

    if file_path in collected:
        return

    collected.add(file_path)

    for module in get_components_dependencies(file_path):

        dep_path = module_to_file(module)

        if dep_path.exists():
            collect_dependencies(dep_path, collected)
        else:
            print(f"WARNING: dependency not found: {module}")


def extract_files(selected_files):
    """
    Copy selected files and their components dependencies.
    """

    files_to_copy = set()

    for file_path in selected_files:
        collect_dependencies(file_path, files_to_copy)

    print("\nFiles to extract:")

    for file_path in sorted(files_to_copy):
        print(f"  - {file_path}")

        relative = file_path.relative_to(PROJECT_ROOT)

        destination = BUILD_ROOT / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(file_path, destination)