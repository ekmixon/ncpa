import os
import shutil
import subprocess
import sys

buildtype = sys.argv[1] if len(sys.argv) > 1 else 'release'
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nsi_store = os.path.join(basedir, 'agent', 'build_resources', 'ncpa.nsi')
nsi = os.path.join(basedir, 'agent', 'build', 'ncpa.nsi')
nsis = os.path.join(os.environ['PROGRAMFILES(X86)'] if os.environ.has_key('PROGRAMFILES(X86)') else os.environ['PROGRAMFILES'], 'NSIS', 'makensis.exe')

os.chdir(basedir)

with open('VERSION') as version_file:
    version = version_file.readline().strip()

try:
    os.remove(os.path.join(basedir, 'build', f'ncpa-{version}.exe'))
except:
    pass

# Building nightly versions requires a git pull and pip upgrade
if buildtype == 'nightly':
	subprocess.Popen(['git', 'pull']).wait()
	subprocess.Popen(['pip', 'install', '--upgrade', '-r', os.path.join(basedir, 'build', 'resources', 'require.txt')]).wait()

# Remove old build
subprocess.Popen(['rmdir', os.path.join(basedir, 'agent', 'build'), '/s', '/q'], shell=True).wait()

os.chdir('agent')

if not os.path.exists('var'):
    os.mkdir('var')

if not os.path.exists('plugins'):
    os.mkdir('plugins')

sys.path.append(os.getcwd())
subprocess.Popen(['python', 'setup_windows.py', 'build_exe']).wait()

environ = os.environ.copy()
environ['NCPA_BUILD_VER'] = version
if not version[-1].isdigit():
	x = version.rsplit('.', 1)
	environ['NCPA_BUILD_VER_CLEAN'] = x[0]
else:
	environ['NCPA_BUILD_VER_CLEAN'] = version
shutil.copy(nsi_store, nsi)
b = subprocess.Popen([nsis, nsi], env=environ)
b.wait()

shutil.copyfile(
    os.path.join(basedir, 'agent', 'build', f'ncpa-{version}.exe'),
    os.path.join(basedir, 'build', f'ncpa-{version}.exe'),
)
