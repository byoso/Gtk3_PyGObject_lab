
import os
import ast




def get_tree(path):
    tree = {}
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and not item.startswith("_") and not item.startswith("."):
            tree[item] = get_tree(item_path)
        elif item.endswith(".py") and not item.startswith("_") and not item.startswith("."):
            tree[item] = None
    return tree
