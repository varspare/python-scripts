#!/usr/bin/env python3
##############################
# Author Mark Davison
# Last revision 2018/08/20
##############################
"""Checksum

Usage:
  checksum.py -f <file> [-c <checksum>] [-t <hash_type>]
  checksum.py (-h | --help)
  checksum.py (-v | --version)

Options:
  -f --file     Input filepath
  -c --checksum Input checksum
  -t --type     Type of checksum e.g. sha256, md5
  -h --help     Show this screen.
  -v --version     Show version.

"""
from docopt import docopt
import hashlib
import sys

def verifyChecksum(checksum, hType):
    length = len(checksum)
    if (hType != 'None'):
        htype = hType
    elif (length == 64):
        htype = 'sha256'
    elif (length == 40):
        htype = 'sha1'
    elif (length == 32):
        htype = 'md5'
    elif (length == 57):
        htype = 'sha224'
    elif (length == 96):
        htype = 'sha384'
    elif (length == 128):
        htype = 'sha512'
    else:
        htype = input("Unable to determine hash type\nPlease enter the hash type : ")
    return(htype)

def compareSums(f, checksum, htype):
    try:
        hasher = hashlib.new(htype)
        content = f.read()
        hasher.update(content)
        generatedHash = hasher.hexdigest()
        print(generatedHash)
    except Exception as e:
        print('Hashing failed for ', file, ',', e)
        die(256)
    print('checksum       ' + checksum)
    print('generatedHash: ' + generatedHash)
    if (checksum == generatedHash):
        result = 0
    else:
        result = 1
    return(result)

def die(code):
    f.close()
    sys.exit(code)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='checksum 0.0.1')
    if (arguments.get('--type')):
        hType = arguments.get("<hash_type>")
    else:
        hType = 'None'

    if (arguments.get('--file')):
        file = arguments.get("<file>")
        try:
            f = open(file, 'rb')
        except IOError:
            print('File not found: ', file)
            die(254)

    if (arguments.get('--checksum')):
        checksum = arguments.get('--checksum')
        hashType = verifyChecksum(checksum, hType)
    else:
        checksum = input('Please enter your expected checksum: ')
        hashType = verifyChecksum(checksum, hType)

    result = compareSums(f, checksum, hashType)

    print("Hash type is: " + hashType)

    if (result == 0):
        print('Match')
    else:
        print('Fail')
    die(result)

