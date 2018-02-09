<b>Symmetric encryption between users of the Hexchat IRC client (http://xchat.org)</b>

The goal with this experiment/project was to as simple and slim as possible with only one script-file add symmetric encryption between two or more IRC users sharing the same password file. To keep it simple without the need of installing external python libraries the script uses the openssl-command-line-client (https://wiki.openssl.org/index.php/Manual:Enc(1)) for encryption and decryption using 256 bit AES-CBC encryption. 


<b>Installation:</b>

Place <i>enc.py</i> in ~/.config/hexchat/addons. Create a passwordfile where the first line of the file is the password (https://www.openssl.org/docs/man1.0.1/apps/openssl.html) and share it with the other part. Change the line: <i>'PASSFILE = "/home/user/pass.key"'</i> in enc.py to the correct path.

<b>How to use:</b>

Enable outgoing encryption in a private dialog window with the command: <i>/enc enable</i>. If encryption is not enabled and an encrypted message is received the encryption/decryption mechanism is automatically enabled. Text changes to green.

<i>/enc enable   - Encrypt outgoing messages on current dialog window </i><br>
<i>/enc disable  - Disable encryption of outgoing messages on current dialog window</i> <br>
<i>/enc info     - Print status about debug/encryption</i>

HexChat Python Interface: http://hexchat.readthedocs.io/en/latest/script_python.html#autoloading-modules
