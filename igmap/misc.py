import os
from shutil import which
from sys import platform

CORES = os.cpu_count()
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


if platform == 'linux' or platform == 'linux2':
    ZCAT_CMD = 'zcat'
    VIDJIL_CMD = 'vidjil-algo_linux'
    IGBLAST_CMD = 'igblastn_linux'
elif platform == 'darwin':
    ZCAT_CMD = 'gzcat'
    VIDJIL_CMD = 'vidjil-algo_darwin'
    IGBLAST_CMD = 'igblastn_darwin'
elif platform == 'win32':
    raise 'Cannot run on Windows'


def CAT_CMD(fname):
    if isinstance(fname, list):
        # TODO warn if extension don't match
        fname = ' '.join(fname)
    if fname.endswith('.gz'):
        return ZCAT_CMD + ' ' + fname
    else:
        return 'cat ' + fname

    
FQ2FA_CMD = '{if(NR%4==1) {printf(">%s\\n",substr($0,2));} else if(NR%4==2) print;}'
FQ2FA_CMD = f'awk \'{FQ2FA_CMD}\' | tr -s \' \' \';\''
TAB2FQ_CMD = '{ if (NF<4) print "@"$1"\\n"$2"\\n+\\n"$3; else print "@"$1"\\n"$2"\\n+\\n"$3"\\n@"$1"\\n"$4"\\n+\\n"$5 }'
TAB2FQ_CMD = f'awk -F"\t" \'{TAB2FQ_CMD}\''


if not which('parallel'):
    raise 'Requires GNU Parallel to work'


EXT_PATH = os.path.abspath(SCRIPT_PATH + '/external')
BIN_PATH = EXT_PATH + '/bin'
if os.path.exists(BIN_PATH + '/vidjil-algo'):
    VIDJIL_CMD = BIN_PATH + '/vidjil-algo'
else:
    VIDJIL_CMD = BIN_PATH + '/' + VIDJIL_CMD
if os.path.exists(BIN_PATH + '/igblastn'):
    IGBLAST_CMD = BIN_PATH + '/igblastn'
else:
    IGBLAST_CMD = BIN_PATH + '/' + IGBLAST_CMD
VIDJIL_DATA_PATH = EXT_PATH + '/vidjil-germline'
IGBLAST_DATA_PATH = EXT_PATH + '/igblast_database'
os.environ['IGDATA'] = os.path.abspath(IGBLAST_DATA_PATH)
IGOR_DATA_PATH = EXT_PATH + '/igor_models'
