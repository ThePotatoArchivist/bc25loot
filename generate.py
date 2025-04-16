import json
import os
import shutil
from os import path, listdir
from os.path import basename
from glob import glob

def parse_single(line: str):
    item, = line.split(' ')
    return {
        'type': 'minecraft:item',
        'name': item,
    }
    
def parse_constant(line: str):
    count_str, item = line.split(' ')
    count = int(count_str)
    return {
        'type': 'minecraft:item',
        'name': item,
        'functions': [
            {
                'function': 'minecraft:set_count',
                'count': count
            }
        ]
    }

def parse_uniform(line: str):
    min_str, max_str, item = line.split(' ')
    imin = int(min_str)
    imax = int(max_str)
    return {
        'type': 'minecraft:item',
        'name': item,
        'functions': [
            {
                'function': 'minecraft:set_count',
                'count': {
                    'type': 'minecraft:uniform',
                    'min': imin,
                    'max': imax,
                }
            }
        ]
    }

def parse_component(line: str):
    index = line.find(' ')
    item = line[:index]
    component = line[index+1:]
    return {
        'type': 'minecraft:item',
        'name': item,
        'functions': [
            {
                'function': 'minecraft:set_components',
                'components': json.loads(component)
            }
        ]
    }

def parse(line: str):
    for parser in parse_single, parse_constant, parse_uniform, parse_component:
        try:
            return parser(line)
        except:
            pass
    raise Exception(line)

target = 'pvploot/data/bc25/loot_table/chests'

def main():
    try:
        os.makedirs(target, exist_ok = False)
    except FileExistsError:
        pass
    
    for filename in listdir(target):
        file_path = path.join(target, filename)
        if path.isfile(file_path):
            os.remove(file_path)
    
    for filename in glob('src/*.txt'):
        with open(filename, 'r') as file:
            lines = list(filter(None, file.read().split('\n')))
        entries = [parse(line) for line in lines]
        with open(path.join(target, path.splitext(basename(filename))[0] + '.json'), 'w') as file:
            file.write(json.dumps({
                'type': 'minecraft:chest',
                'pools': [
                    {
                        'rolls': 1,
                        'entries': entries
                    }
                ]
            }, indent=2))
            
    for filename in glob('src/static/*'):
        shutil.copyfile(filename, path.join(target, basename(filename)))
    
if __name__ == '__main__':
    main()