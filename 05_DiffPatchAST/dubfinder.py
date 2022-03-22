import sys
import inspect
import ast
from importlib import import_module
from textwrap import dedent
from difflib import SequenceMatcher

modules_methods = {}
attrs_to_change = ('name', 'id', 'arg', 'attr')

def find_functions(mod_name, mod):

    for name, obj in inspect.getmembers(mod):
        
        if inspect.isclass(obj):
            if name[:2] != '__':
                find_functions(mod_name + '.' + name, obj)
            continue

        if inspect.ismethod(obj) or inspect.isfunction(obj):
            val = dedent(inspect.getsource(obj))
            ast_tree = ast.parse(val)

            for node in ast.walk(ast_tree):
                for attr in attrs_to_change:
                    if hasattr(node, attr):
                        setattr(node, attr, '_')
        
            modules_methods[mod_name + '.' + name] = ast.unparse(ast_tree)

for module_name in sys.argv[1:]:
    module = import_module(module_name)
    find_functions(module_name, module)

keys = sorted(list(modules_methods.keys()), key=str.lower)

for i in range(len(keys)):
    for j in range(i + 1, len(keys)):

        ratio = SequenceMatcher(None, 
                                modules_methods[keys[i]],
                                modules_methods[keys[j]]).ratio()

        if ratio > 0.95:
            print(keys[i], keys[j])
