import os
from configparser import ConfigParser
config= ConfigParser()
config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','config.ini')))

params= config['DEFAULT']
unu = params['unu']
ConvertBetweenFileFormats= params['ConvertBetweenFileFormats']
bet = params['bet']
eta= params['BrainMaskingThreshold']

dwiPath="~/Downloads/maskTest/1001-dwi-xc.nrrd"
prefix='1001-dwi-xc'
directory='~/Downloads/maskTest/'
fileFormat='nrrd'

from subprocess import check_call, check_output
check_output(['sh', 'createMask.sh',
            '-i', dwiPath,
            '-f', fileFormat,
            '-p', prefix,
            '-o', directory,
            '-e', eta,
            '-b', bet,
            '-u', unu,
            '-c', ConvertBetweenFileFormats])

# from plumbum import FG
# ('sh', 'createMask.sh',
#             '-i', dwiPath,
#             '-f', fileFormat,
#             '-p', prefix,
#             '-o', directory,
#             '-e', eta,
#             '-b', bet,
#             '-u', unu,
#             '-c', ConvertBetweenFileFormats) & FG
