## ECIES
Matthew Bernardo

ECIES based public/private key pair encryption using simple CLI interface

User is presented with a menu upon running

- SECP_256k1 is used to generate public/private keys
- SHA256 is used as the KDF
- AES-SIV is used to encrypt/decrypt the actual file

NOTE:
- plaintext file must be created beforehand
- this file automatically creates peer and user keys for the sake of simplicity

### USAGE

python ecies.py

### Example Output

Assume we have a plaintext file plaintext.txt that contains:
```
hi this is some plaintext
multi line test
another line
```
Starting the program...

```
ECIES
Matthew Bernardo
Menu:
	 new 	 New Identity(new user public key)
	 peer 	 New peer identity
	 enc 	 encrypt a file to a target public key
	 dec 	 decrypt a file
	 my 	 my public key
	 peer 	 user public key
	 menu 	 show menu
	 exit 	 exits program

enter an option: new
input desired name: alice

Generating new key for alice using SECP_256k1
private key: 6353112a7335240bf0521dae3a72d72a6000e62d2fcc813d0784e16970e6b76c
public key: 34899fafa96a96aa35591d2631a1cfe1c1d47d21faf2fe6bea3b18d25913aa87

enter an option: peer
input desired name: bob

Generating new key for bob using SECP_256k1
private key: f7f21c364adbcf8fd54f40ef7e3ee6787e88daedd52d1309253e13fe6b992ddb
public key: 012ba44b2cd21d582217b8c8fb8fc97d8aebdfbb7c5b5d1ab0050cd5a7a92ec1

enter an option: enc
enter plaintext file to encrypt: plaintext.txt
enter outputfile to write to: cipherout
finished encrypting plaintext.txt to cipherout

enter an option: dec
enter ciphertext file to decrypt: cipherout
enter outputfile to write to: plainout
finished decrypting cipherout to plainout

enter an option: exit
```

the output of cipherout is:
```
d53980a2b6859debc7ee45bbb2bdb5674f3bb2829cfd594badd718d052cd8691082b9bdf2bd27c58b6
62e2d2b6289a38814ba069f916eafd7740aedc2a0475010347b53ffd072898
dd6c359ff0c7af988088f6784b410af32699c8453797324e72494e11
```
the output of plainout is:
```
hi this is some plaintext
multi line test
another line
```

ECIES Encryption and Decryption success!