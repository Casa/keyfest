#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Casa KeyFest 2021
# Key Generation Demo
# Author: Ron Stoner
# Crypto libraries provided by https://github.com/circulosmeos/bitcoin-in-tiny-pieces
#

from colorama import init, Fore, Back, Style
from bitcoin import *
import os
import sys
import subprocess

version = '1.4'
# 1.0 - Initial code creation
# 1.1 - Added in simple style sha256 key generation
# 1.2 - Added in more secure ECDSA key generation
# 1.3 - Added title screen and selection menu
# 1.4 - Added random key generation from os.urandom

# Colors for console
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Print the title screen
def print_title_screen():
    print(Fore.MAGENTA + Back.WHITE)
    print('████████████████████████████████████████')
    print('████████████████████████████████████████')
    print('████████████████████████████████████████')
    print('████████████████████                 ███')
    print('█████████████████                       ')
    print('████████████████       ███████████      ')
    print('██████████████       ██████████████     ')
    print('██████████████      ████████████████████')
    print('██████████████      ████████████████████')
    print('██████████████      ████████████████████')
    print('███████████████      ██████████████     ')
    print('████████████████        █████████       ')
    print('█████████████████                      █')
    print('█████████████████████                ███')
    print('████████████████████████████████████████')
    print('████████████████████████████████████████' + Fore.RESET + Back.RESET + Style.BRIGHT)
    print('         [ Casa KeyFest 2021  ]')
    print('           [  Keygen Demo  ]')
    print('' + Style.RESET_ALL)

def gen_simple_key():
    # ***INSECURE***
    # DO NOT USE THIS FOR FUNDS!
    key_input = input('\nEnter a word, passphrase, lyric, or quote: ')
    privkey = sha256(key_input)
    pubkey = privtopub(privkey)
    address = pubtoaddr(pubkey) #Uncompressed
    #wif = subprocess.run(['./lib/bitcoin-wif-from-private-key.py', privkey])
    print('\n📝 Input:       ' + str(key_input))
    print('🔐 Seed:        ' + str(privkey))
    print('🔑 Pub Key:     ' + str(pubkey))
    #print(' WiF:        ' + str(wif))
    print('₿  Address:     ' + str(address))

def gen_secure_key():
    # More secure, but still not great
    # TODO: Use multiple sources for entropy or better yet, hardware wallets
    # ECDSA = y^2 = x^2 + ax + b
    key_input = input('\nEnter a 64 byte private key or press enter for random: ')

    # Check to see if private key is 32 bytes
    # Commented out for demo
    #if len(key_input) != 64:
    #    print('Incorrect key size!\n')
    #    return

    # Check if user wants a random key
    if not key_input:
        #print('\nGenerating random key from os.urandom')
        key_input = os.urandom(32).hex()
        #print(key_input)

    pub_key = subprocess.Popen(['./lib/bitcoin-public-from-private.py', key_input], stdout=subprocess.PIPE)
    subprocess.run(['./lib/bitcoin-address-from-public-key.py'], stdin=pub_key.stdout)

def main():
    #Clear screen
    os.system('clear')

    #Init colorama
    init()

    #Print title screen
    print_title_screen()

    while True:
        #Get user input for key generation
        selection = input('\n 1) Generate an insecure brainwallet keyset\n 2) Generate a more secure ECDSA keyset\n 3) Exit\n')
        if selection == '1':
            gen_simple_key()
        elif selection == '2':
            gen_secure_key()
        elif selection == '3':
            sys.exit()

if __name__ == '__main__':
    main()
    sys.exit()
