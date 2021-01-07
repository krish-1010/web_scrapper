import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package]) 

install('beautifulsoup4')

install('requests')

install('parse')

install('db-sqlite3')

install('pandas')