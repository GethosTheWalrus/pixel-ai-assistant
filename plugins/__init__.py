import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    moduleString = module[:-3]
    string = f'from plugins.{moduleString} import {moduleString}'
    exec(string)
del module
