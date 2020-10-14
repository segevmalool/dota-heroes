import numpy as np
import re
import json

def parseDotaHeroes(npc_heroes_filename):
    with open(npc_heroes_filename, 'r') as hero_fp:
        heroes_lines = [line.strip() for line in hero_fp.readlines()]

    heroes_lines = list(map(lambda line: re.sub('//.{0,}','',line), heroes_lines))
    heroes_lines = list(filter(lambda line: not line == '', heroes_lines))
    heroes_lines = [line.strip('\t') for line in heroes_lines]
    heroes_lines = [line.strip() for line in heroes_lines]
    heroes_lines = [re.sub('[ ]{1,}','\t',line) for line in heroes_lines]
    heroes_lines = [re.sub('[\t]{1,}',':',line) for line in heroes_lines]

    heroes_lines_no_singletons = []
    i = 0
    while i < len(heroes_lines):
        if i != len(heroes_lines)-1 and heroes_lines[i+1] == '{':
            heroes_lines_no_singletons.append(heroes_lines[i] + ':' + '{')
            i += 2
        else:
            heroes_lines_no_singletons.append(heroes_lines[i])
            i += 1
     
    heroes_json_string = ''
    i = 0
    
    while i < len(heroes_lines_no_singletons):
        if i == len(heroes_lines_no_singletons)-1 or heroes_lines_no_singletons[i].endswith(':{') or heroes_lines_no_singletons[i+1] == '}':
            heroes_json_string += heroes_lines_no_singletons[i]
        else:
            heroes_json_string += heroes_lines_no_singletons[i] + ','
        i += 1

    heroes_json_string = '{' + heroes_json_string + '}'

    dota_heroes = json.loads(heroes_json_string)['DOTAHeroes']

    dota_heroes.pop('npc_dota_hero_base')
    dota_heroes.pop('npc_dota_hero_target_dummy')
    version = dota_heroes.pop('Version')
    
    return dota_heroes
    
if __name__ == '__main__':
    npc_heroes = r"S:\SteamLibrary\steamapps\common\dota 2 beta\game\dota\scripts\npc\npc_heroes.txt"
    
    npc_heroes_json = parseDotaHeroes(npc_heroes)
    
    with open('npc_heroes.json', 'w') as hero_fp:
        hero_fp.write(json.dumps(npc_heroes_json))
        
    print('npc_heroes.txt converted to npc_heroes.json')