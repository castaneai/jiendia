import os

def get_latale_directory_path():
    pf = os.environ['ProgramFiles(x86)'] if 'ProgramFiles(x86)' in os.environ else os.environ['ProgramFiles']
    return pf + '/Gamepot/LaTale'
