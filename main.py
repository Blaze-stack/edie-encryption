from logging import debug
import subprocess
import re
from collections import Counter
import string
from string import punctuation
from math import sqrt
import base64
import hashlib
import sys
import csv
import array as arr
import time
from alpaca_trade_api.entity import Trade
from colorama import Fore
import os
from random import randint
filedata = []
class f:
    def dec_to_bin_8bit(val):
        binary = '00000000'

        if val >= 128:
            binary = binary[:0] + '1' + binary[:7]
            val -= 128
        else:
            binary = binary[:0] + '0' + binary[:7]
        if val >= 64:
            binary = binary[:1] + '1' + binary[:6]
            val -= 64
        else:
            binary = binary[:1] + '0' + binary[:6]
        if val >= 32:
            binary = binary[:2] + '1' + binary[:5]
            val -= 32
        else:
            binary = binary[:2] + '0' + binary[:5]
        if val >= 16:
            binary = binary[:3] + '1' + binary[:4]
            val -= 16
        else:
            binary = binary[:3] + '0' + binary[:4]
        if val >= 8:
            binary = binary[:4] + '1' + binary[:3]
            val -= 8
        else:
            binary = binary[:4] + '0' + binary[:3]
        if val >= 4:
            binary = binary[:5] + '1' + binary[:2]
            val -= 4
        else:
            binary = binary[:5] + '0' + binary[:2]
        if val >= 2:
            binary = binary[:6] + '1' + binary[:1]
            val -= 2
        else:
            binary = binary[:6] + '0' + binary[:1]
        if val >= 1:
            binary = binary[:7] + '1' + binary[:0]
            val -= 1
        else:
            binary = binary[:7] + '0' + binary[:0]

        return binary



    def two_char_to_bin(val1, val2):
        binary = '00000000'
        if val1 >= 8:
            binary = binary[:0] + '1' + binary[:7]
            val1 -= 8
        else:
            binary = binary[:0] + '0' + binary[:7]
        if val1 >= 4:
            binary = binary[:1] + '1' + binary[:6]
            val1 -= 4
        else:
            binary = binary[:1] + '0' + binary[:6]
        if val1 >= 2:
            binary = binary[:2] + '1' + binary[:5]
            val1 -= 2
        else:
            binary = binary[:2] + '0' + binary[:5]
        if val1 >= 1:
            binary = binary[:3] + '1' + binary[:4]
            val1 -= 1
        else:
            binary = binary[:3] + '0' + binary[:4]
        if val2 >= 8:
            binary = binary[:4] + '1' + binary[:3]
            val2 -= 8
        else:
            binary = binary[:4] + '0' + binary[:3]
        if val2 >= 4:
            binary = binary[:5] + '1' + binary[:2]
            val2 -= 4
        else:
            binary = binary[:5] + '0' + binary[:2]
        if val2 >= 2:
            binary = binary[:6] + '1' + binary[:1]
            val2 -= 2
        else:
            binary = binary[:6] + '0' + binary[:1]
        if val2 >= 1:
            binary = binary[:7] + '1' + binary[:0]
            val2 -= 1
        else:
            binary = binary[:7] + '0' + binary[:0]
        return binary



    #this function convert 8 bit binary or a byte to integer, here the binary argument is string of 8 char
    # representing '1's and '0's
    def bin_to_dec(binary):
        val = 0
        if binary[0] == '1':
            val += 128
        if binary[1] == '1':
            val += 64
        if binary[2] == '1':
            val += 32
        if binary[3] == '1':
            val += 16
        if binary[4] == '1':
            val += 8
        if binary[5] == '1':
            val += 4
        if binary[6] == '1':
            val += 2
        if binary[7] == '1':
            val += 1
        return val


    #here the process of substitution is done for the encryption, meaning replacing a number with some another number,
    # the tabel is given as follow

    # 1   ->  14
    # 2   ->  15
    # 3   ->  5
    # 4   ->  9
    # 5   ->  11
    # 6   ->  6
    # 7   ->  13
    # 8   ->  2
    # 9   ->  4
    # 10  ->  8
    # 11  ->  1
    # 12  ->  3
    # 13  ->  10
    # 14  ->  7
    # 15  ->  12
    def substitution(num):
        if num == 1:
            val = 14
        elif num == 2:
            val = 15
        elif num == 3:
            val = 5
        elif num == 4:
            val = 9
        elif num == 5:
            val = 11
        elif num == 6:
            val = 6
        elif num == 7:
            val = 13
        elif num == 8:
            val = 2
        elif num == 9:
            val = 4
        elif num == 10:
            val = 8
        elif num == 11:
            val = 1
        elif num == 12:
            val = 3
        elif num == 13:
            val = 10
        elif num == 14:
            val = 7
        elif num == 15:
            val = 12
        else:
            val = 0
        return val


    #here the process of permutation is done aka interchanging the places of bit in a byte,
    # the sequence of binary arrangement as follow

    # 1  ->  5
    # 2  ->  8
    # 3  ->  6
    # 4  ->  3
    # 5  ->  2
    # 6  ->  4
    # 7  ->  1
    # 8  ->  7
    def permutation(binaryIn):
        binary = '00000000'
        binary = binary[:0] + binaryIn[4] + binary[:7]
        binary = binary[:1] + binaryIn[7] + binary[:6]
        binary = binary[:2] + binaryIn[5] + binary[:5]
        binary = binary[:3] + binaryIn[2] + binary[:4]
        binary = binary[:4] + binaryIn[1] + binary[:3]
        binary = binary[:5] + binaryIn[3] + binary[:2]
        binary = binary[:6] + binaryIn[0] + binary[:1]
        binary = binary[:7] + binaryIn[6] + binary[:0]
        return binary



    #it converts 4 bit binary to int, again the binary is a string of '0' and '1'
    def bin_to_dec_4bit(binary):
        val = 0
        if binary[0] == '1':
            val += 8
        if binary[1] == '1':
            val += 4
        if binary[2] == '1':
            val += 2
        if binary[3] == '1':
            val += 1
        return val



    #it converts int to 4 bit binary, the return binary is in form of a string
    def dec_to_bin_4bit(val):
        binary = '0000'
        if val >= 8:
            binary = binary[:0] + '1' + binary[:3]
            val -= 8
        else:
            binary = binary[:0] + '0' + binary[:3]
        if val >= 4:
            binary = binary[:1] + '1' + binary[:2]
            val -= 4
        else:
            binary = binary[:1] + '0' + binary[:2]
        if val >= 2:
            binary = binary[:2] + '1' + binary[:1]
            val -= 2
        else:
            binary = binary[:2] + '0' + binary[:1]
        if val >= 1:
            binary = binary[:3] + '1' + binary[:0]
            val -= 1
        else:
            binary = binary[:3] + '0' + binary[:0]
        return binary



    #here the process of reverse permutation is done for the decryption. It shoud be exact reverse of
    # the perutation process, binary interchange sequence as follow

    # 1  ->  7
    # 2  ->  5
    # 3  ->  4
    # 4  ->  6
    # 5  ->  1
    # 6  ->  3
    # 7  ->  8
    # 8  ->  2
    def reverse_permutation(binaryIn):
        binary = '00000000'
        binary = binary[:0] + binaryIn[6] + binary[:7]
        binary = binary[:1] + binaryIn[4] + binary[:6]
        binary = binary[:2] + binaryIn[3] + binary[:5]
        binary = binary[:3] + binaryIn[5] + binary[:4]
        binary = binary[:4] + binaryIn[0] + binary[:3]
        binary = binary[:5] + binaryIn[2] + binary[:2]
        binary = binary[:6] + binaryIn[7] + binary[:1]
        binary = binary[:7] + binaryIn[1] + binary[:0]
        return binary


    #here the process of reverse substitution is done for the decryption. Make sure it is exact
    # reverse if the substitution process. Sequence of number interchange as follow

    # 1   ->  11
    # 2   ->  8
    # 3   ->  12
    # 4   ->  9
    # 5   ->  3
    # 6   ->  6
    # 7   ->  14
    # 8   ->  10
    # 9   ->  4
    # 10  ->  13
    # 11  ->  5
    # 12  ->  15
    # 13  ->  7
    # 14  ->  1
    # 15  ->  2
    def reverse_substitution(num):
        if num == 1:
            val = 11
        elif num == 2:
            val = 8
        elif num == 3:
            val = 12
        elif num == 4:
            val = 9
        elif num == 5:
            val = 3
        elif num == 6:
            val = 6
        elif num == 7:
            val = 14
        elif num == 8:
            val = 10
        elif num == 9:
            val = 4
        elif num == 10:
            val = 13
        elif num == 11:
            val = 5
        elif num == 12:
            val = 15
        elif num == 13:
            val = 7
        elif num == 14:
            val = 1
        elif num == 15:
            val = 2
        else:
            val = 0
        return val


def decrpyt(encrypted):
    try:
        alphabet = {
            '\u0316' : "a",
            '\u0317' : "b",
            '\u0318' : "c",
            '\u0319' : "d",
            '\u031C' : "e",
            '\u031D' : "f",
            '\u031E' : "g",
            '\u031F' : "h",
            '\u0320' : "i",
            '\u0324' : "j",
            '\u0325' : "k",
            '\u0326' : "l",
            '\u0329' : "m",
            '\u032A' : "n",
            '\u032B' : "o",
            '\u032C' : "p",
            '\u032D' : "q",
            '\u032E' : "r",
            '\u032F' : "s",
            '\u0330' : "t",
            '\u0331' : "u",
            '\u0332' : "v",
            '\u0333' : "w",
            '\u0339' : "x",
            '\u033A' : "y",
            '\u033B' : "z",
            '\u030D' : "A",
            '\u030E' : "B",
            '\u0304' : "C",
            '\u0305' : "D",
            '\u033F' : "E",
            '\u0311' : "F",
            '\u0306' : "G",
            '\u0310' : "H",
            '\u0352' : "I",
            '\u0357' : "J",
            '\u0351' : "K",
            '\u0307' : "L",
            '\u0308' : "M",
            '\u030A' : "N",
            '\u0342' : "O",
            '\u0343' : "P",
            '\u0344' : "Q",
            '\u034A' : "R",
            '\u034B' : "S",
            '\u034C' : "T",
            '\u0303' : "U",
            '\u0302' : "V",
            '\u030C' : "W",
            '\u0350' : "X",
            '\u0300' : "Y",
            '\u0301' : "Z",
            '\u0315' : "0",
            '\u031B' : "1",
            '\u0340' : "2",
            '\u0341' : "3",
            '\u0358' : "4",
            '\u0321' : "5",
            '\u0322' : "6",
            '\u0327' : "7",
            '\u0328' : "8",
            '\u0334' : "9",
            '\u0335' : "=",
            '\u0336' : '+',
            '\u034F' : '/',
            '\u035C' : '\\',
            '\u035D' : 'Í',
        }

        map = {
            "ᚨ": "a",
            "ᛒ": "b",
            "ᚲ": "c",
            "ᛞ": "d",
            "ᛖ": "e",
            "ᚠ": "f",
            "ᚷ": "g",
            "ᚺ": "h",
            "ᛁ": "i",
            "ᛃ": "j",
            "ᚴ": "k",
            "ᛚ": "l",
            "ᛗ": "m",
            "ᚾ": "n",
            "ᛟ": "o",
            "ᛈ": "p",
            "ᛩ": "q",
            "ᚱ": "r",
            "ᛋ": "s",
            "ᛏ": "t",
            "ᚢ": "u",
            "ᚡ": "v",
            "ᚹ": "w",
            "ᛪ": "x",
            "ᚤ": "y",
            "ᛉ": "z"
        }
    

        encrypted = encrypted.replace(" ", "")
        decrypted = ""

        for letters in encrypted:
            try:
                decrypted += alphabet[letters]
            except:
                decrypted += letters

        decrypted_decoded = ""

        for i in decrypted:
            if i == i.lower():
                decrypted_decoded += i.upper()
            elif i == i.upper():
                decrypted_decoded += i.lower()
            else:
                decrypted_decoded += i

        decrypted = base64.b64decode(decrypted_decoded.encode("utf-8"))
        decrypted = decrypted.decode("utf-8")
        oge = ""
        for let in decrypted:
            try:
                oge += map[let]
            except:
                oge += let
        decrypted = base64.b64decode(oge.encode("utf-8"))
        decrypted = decrypted.decode("utf-8")

        keynumb = int(decrypted[:1])
        key = decrypted[-keynumb:]
        decrypted = decrypted[1:-keynumb]
        forward = 0
        backward = len(decrypted) - 1
    
        for i in decrypted:
            pos = len(key) - 1
            if 256 <= ord(i) <= 288:
                k = ord(i) - 256
                i = chr(k)

            if 289 <= ord(i) <= 322:
                k = ord(i) - 162
                i = chr(k)

            for j in key:
                binary = f.reverse_permutation(f.dec_to_bin_8bit(ord(i) ^ ord(key[pos])))
                i = chr(f.bin_to_dec(f.dec_to_bin_4bit(f.reverse_substitution(f.bin_to_dec_4bit(binary[0:4]))) + f.dec_to_bin_4bit(
                    f.reverse_substitution(f.bin_to_dec_4bit(binary[4:8])))))
                pos -= 1
            decrypted = decrypted[:forward] + i + decrypted[:backward]
            forward += 1
            backward -= 1

        return decrypted
    except:
        print(f'{Fore.WHITE}[ {Fore.CYAN}\u00A7 {Fore.WHITE}] {Fore.LIGHTBLACK_EX} | An error as occured')

def encrypt(og):
    try:
        forward = 0
        backward = len(og) - 1
        keynumb = randint(2, 3)
        key = og[::keynumb]
        keylen = len(key)
        for i in og:
        
            for j in key:

                val1, val2 = 0, 0
                bin_val = f.dec_to_bin_8bit(ord(i))
            
                if bin_val[0] == '1':
                    val1 += 8
                if bin_val[1] == '1':
                    val1 += 4
                if bin_val[2] == '1':
                    val1 += 2
                if bin_val[3] == '1':
                    val1 += 1
                
                if bin_val[4] == '1':
                    val2 += 8
                if bin_val[5] == '1':
                    val2 += 4
                if bin_val[6] == '1':
                    val2 += 2
                if bin_val[7] == '1':
                    val2 += 1
                
                i = chr(ord(j) ^ f.bin_to_dec(f.permutation(f.two_char_to_bin(f.substitution(val1), f.substitution(val2)))))
            
            if ord(i) < 33:
                k = ord(i) + 256
                i = chr(k)
            
            if 126 < ord(i) < 161:
                k = ord(i) + 162
                i = chr(k)
            
            og = og[:forward] + i + og[:backward]
            forward += 1
            backward -= 1
        
        og = str(keylen) + og + key
        alphabet = {
            'a': '\u0316',
            'b': '\u0317',
            'c': '\u0318',
            'd': '\u0319',
            'e': '\u031C',
            'f': '\u031D',
            'g': '\u031E',
            'h': '\u031F',
            'i': '\u0320',
            'j': '\u0324',
            'k': '\u0325',
            'l': '\u0326',
            'm': '\u0329',
            'n': '\u032A',
            'o': '\u032B',
            'p': '\u032C',
            'q': '\u032D',
            'r': '\u032E',
            's': '\u032F',
            't': '\u0330',
            'u': '\u0331',
            'v': '\u0332',
            'w': '\u0333',
            'x': '\u0339',
            'y': '\u033A',
            'z': '\u033B',
            'A': '\u030D',
            'B': '\u030E',
            'C': '\u0304',
            'D': '\u0305',
            'E': '\u033F',
            'F': '\u0311',
            'G': '\u0306',
            'H': '\u0310',
            'I': '\u0352',
            'J': '\u0357',
            'K': '\u0351',
            'L': '\u0307',
            'M': '\u0308',
            'N': '\u030A',
            'O': '\u0342',
            'P': '\u0343',
            'Q': '\u0344',
            'R': '\u034A',
            'S': '\u034B',
            'T': '\u034C',
            'U': '\u0303',
            'V': '\u0302',
            'W': '\u030C',
            'X': '\u0350',
            'Y': '\u0300',
            'Z': '\u0301',
            '0': '\u0315',
            '1': '\u031B',
            '2': '\u0340',
            '3': '\u0341',
            '4': '\u0358',
            '5': '\u0321',
            '6': '\u0322',
            '7': '\u0327',
            '8': '\u0328',
            '9': '\u0334',
            '=': '\u0335',
            '+': '\u0336',
            '/': '\u034F',
            '\\': '\u035C',
            'Í': '\u035D',
        }

        map = {
            "a": "ᚨ",
            "b": "ᛒ",
            "c": "ᚲ",
            "d": "ᛞ",
            "e": "ᛖ",
            "f": "ᚠ",
            "g": "ᚷ",
            "h": "ᚺ",
            "i": "ᛁ",
            "j": "ᛃ",
            "k": "ᚴ",
            "l": "ᛚ",
            "m": "ᛗ",
            "n": "ᚾ",
            "o": "ᛟ",
            "p": "ᛈ",
            "q": "ᛩ",
            "r": "ᚱ",
            "s": "ᛋ",
            "t": "ᛏ",
            "u": "ᚢ",
            "v": "ᚡ",
            "w": "ᚹ",
            "x": "ᛪ",
            "y": "ᚤ",
            "z": "ᛉ"
        }

    
        og = base64.b64encode(og.encode("utf-8"))
        og = og.decode("utf-8")
        oge = ""
        for let in og:
            try:
                oge += map[let]
            except:
                oge += let
        og = base64.b64encode(oge.encode("utf-8"))
        new = ""
        og = og.decode("utf-8")
        ogsplit = []
        ogn = ""
        for i in og:
            if i == i.lower():
                ogn += i.upper()
            elif i == i.upper():
                ogn += i.lower()
            else:
                ogn += i
            ogsplit.append(i)
        for letters in ogn:
            new += f" {alphabet[letters]}"
        return new
    except:
        print(f'{Fore.WHITE}[ {Fore.CYAN}\u00A7 {Fore.WHITE}] {Fore.LIGHTBLACK_EX} | An error as occured')


os.system("cls")
logo = f"""{Fore.CYAN}   _______   ________  ___  _______      
  |\  ___ \ |\   ___ \|\  \|\  ___ \     
  \ \   __/|\ \  \_|\ \ \  \ \   __/|    
   \ \  \_|/_\ \  \ \\\\ \ \  \ \  \_|/__  
    \ \  \_|\ \ \  \_\\\\ \ \  \ \  \_|\ \ 
     \ \_______\ \_______\ \__\ \_______\ \

      \|_______|\|_______|\|__|\|_______| ENCRYPTION"""

print(logo)
print("")
print("")
while True:
    data = ""
    typeLSS = input(f'{Fore.WHITE}[ {Fore.YELLOW}> {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Encrypt or Decrypt  | {Fore.WHITE}E/D  {Fore.LIGHTBLACK_EX}: {Fore.WHITE}')
    if typeLSS.upper() == "E": 
        data = input(f"{Fore.WHITE}[ {Fore.YELLOW}> {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Please enter text to encrypt : {Fore.WHITE}")
        encrypteddata = encrypt(data)
        print(f'{Fore.WHITE}[ {Fore.CYAN}\u00A7 {Fore.WHITE}] {Fore.LIGHTBLACK_EX} | Text has been encrypted')
        print(f'{Fore.WHITE}[ {Fore.CYAN}\u00A7 {Fore.WHITE}] {Fore.LIGHTBLACK_EX} | {Fore.GREEN}{encrypteddata}')
    if typeLSS.upper() == "D":
        data = input(f"{Fore.WHITE}[ {Fore.YELLOW}> {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Please enter text to decrypt : {Fore.WHITE}")
        decrypteddata = decrpyt(data)
        print(f'{Fore.WHITE}[ {Fore.CYAN}\u00A7 {Fore.WHITE}] {Fore.LIGHTBLACK_EX} | Text has been decrypted')
        print(f'{Fore.WHITE}[ {Fore.CYAN}\u00A7 {Fore.WHITE}] {Fore.LIGHTBLACK_EX} | {Fore.GREEN}{decrypteddata}')



