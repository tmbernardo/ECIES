"""
Matthew Bernardo
ECIES
ecies.py

ECIES based public/private key pair encryption using simple CLI interface
User is presented with a menu upon running
NOTE:
  plaintext file must be created beforehand
  this file automatically creates peer and user keys for the sake of simplicity

USAGE: python ecies.py
see readme.md for example
"""
from ecc.curves import SECP_256k1
from ecc.curves import SmallWeierstrassCurveFp
from ecc.ecc import string_to_int, int_to_string
from cipher.aes_siv import AES_SIV
import hashlib
import os
import pwd
import click

user = None
peer = None

class persona:
  def __init__(self, name, private_key, public_key):
    self.name = name
    self.private_key = private_key
    self.public_key = public_key

  def kdf(self, key):
    return hashlib.sha256(int_to_string(key)).hexdigest()

  def key_agree(self, peer_pub):
    return (self.private_key * peer_pub).x

  def kMac(self):
    return self.kdf((self.private_key * self.public_key).x)

  def kEnc(self, peer_pub):
    return self.kdf( self.key_agree(peer_pub) )

def new():

  name = raw_input("input desired name: ")
  
  print("\nGenerating new key for {} using SECP_256k1".format(name))
  curve = SECP_256k1()
  G = curve.generator()
  private = string_to_int( os.urandom(curve.coord_size) )
  public = private * G

  priv_hex = int_to_string(private).encode('hex')
  pub_hex = int_to_string(public.x).encode('hex')
  click.echo( 'private key: {}'.format(priv_hex) )
  click.echo( 'public key: {}\n'.format(pub_hex) )

  return persona(name, private, public)

def encrypt():
  global user, peer
  if (user == None or peer == None):
    print("Missing user or peer")
    return

  kMac = user.kMac()
  kEnc = user.kEnc(peer.public_key)

  aes = AES_SIV(kEnc)

  infile = raw_input("enter plaintext file to encrypt: ").strip()
  outfile = raw_input("enter outputfile to write to: ").strip()

  with open(outfile, "w") as ciphertxt:
    with open(infile, "rb") as plaintxt:
      for line in plaintxt:
        enc = aes.encrypt(line.strip(),[]).encode('hex')
        ciphertxt.write(enc + '\n')
  print("finished encrypting {} to {}\n".format(infile,outfile))

def decrypt():
  global user, peer
  if (user == None or peer == None):
    print("Missing user or peer")
    return

  kMax = peer.kMac()
  kEnc = peer.kEnc(user.public_key)

  aes = AES_SIV(kEnc)

  infile = raw_input("enter ciphertext file to decrypt: ").strip()
  outfile = raw_input("enter outputfile to write to: ").strip()

  with open(infile, "rb") as ciphertxt:
    with open(outfile, "w") as plaintxt:
      for line in ciphertxt:
        cipherline = aes.decrypt(line.strip().decode('hex'),[])
        plaintxt.write(cipherline + '\n')
  print("finished decrypting {} to {}\n".format(infile,outfile))


def newuser():
  global user
  user = new()

def newpeer():
  global peer
  peer = new()

def my():
  if (user == None):
    print("No user")
  print('public key: {}\n'.format(user.public_key))

def peer():
  if (peer == None):
    print("No Peer")
  print('public key: {}\n'.format(peer.public_key))

def printmenu():
  print("Menu:")
  print("\t new \t New Identity(new user public key)")
  print("\t peer \t New peer identity")
  print("\t enc \t encrypt a file to a target public key")
  print("\t dec \t decrypt a file")
  print("\t my \t my public key")
  print("\t peer \t user public key")
  print("\t menu \t show menu")
  print("\t exit \t exits program")

def interactive_menu():
  print("ECIES")
  print("Matthew Bernardo")
  printmenu()

  while True:
    i = raw_input("enter an option: ").strip()
    if (i == "new"):
      newuser()
    elif (i == "peer"):
      newpeer()
    elif (i == "enc"):
      encrypt()
    elif (i == "dec"):
      decrypt()
    elif (i == "my"):
      my()
    elif (i == "peer"):
      peer()
    elif (i == "menu"):
      printmenu()
    elif (i == "exit"):
      break
    else:
      print("command not found")

if __name__ == '__main__':
    interactive_menu()
