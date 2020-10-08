#!/usr/bin/env python3

def quote(bs):
    o = b''
    for c in bs:
        # Control char or !, :, and ;
        if c <= 0x1f or c == 0x21 or c == 0x3a or c == 0x3b :
            o += b'!' + bytes([c+0x20])
        # First part of the 8-bit range
        elif c >= 0x7f and c <= 0xcf:
            o += b':' + bytes([c-0x5f])
        # Second part of the 8-bit range
        elif c >= 0xd0:
            o += b';' + bytes([c-0xb0])
        else:
            o += bytes([c])
    return o

def unquote(bs, callback = None):
    o = b''
    bang = False
    colon = False
    semicolon = False

    for c in bs:
        if not (bang or colon or semicolon):
            if c == 0x21:
                bang = True
                continue
            elif c == 0x3a:
                colon = True
                continue
            elif c == 0x3b:
                semicolon = True
                continue
        if bang:
            o += bytes([c-0x20])
            bang = False
        elif colon:
            o += bytes([c+0x5f])
            colon = False
        elif semicolon:
            n = c+0xb0
            if n > 0xff:
                b = bytes([c])
                if callback is not None:
                    callback(b, o)
            else:
                o += bytes([n])
            semicolon = False
        else:
            o += bytes([c])
    return o

def cb(b, o):
    print(f"Callback with special {b} and current output of {o}")

c = """This test, if you want to call it that.\xff\x7f\x00\r\n5,6,7 ,8\rIs a test of the extrema! -- and other random chars; like these: $1.40 / 1#\n""".encode('latin1')
print("==== Original as bytes====")
print(c)
print()
q = quote(c)
q = q[:53] + b';~' + q[53:]
print("==== Quoted (with inserted in-band signal) ====")
print(q)
print()
print("==== Unquoting ====")
u = unquote(q, cb)
print()
print("==== Unqoted bytes ====")
print(u)
print()
