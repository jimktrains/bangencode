# bangencode

**Please consider the specification below to be freely available. The AGPL3
applies specifically to the reference implementation.**

## Specification

`bangencode` is a 7-bit safe string encoding which preserves the
printable characters and efficiently encodes the remaining. The basic
premise is using an escape character to shift the range (switch
alphabets) that the printable ascii characters represent. The shifts are
as follows:

|prefix|offset to following character|input range|output range|
|------|-----------------------------|-----------|------------|
|!|-0x20|[0x00, 0x1f], 0x21, 0x3a, 0x3b |[0x20, 0x3f], 0x41, 0x5a, 0x5b|
|:| 0x5F|[0x7f, 0xcf] |[0x20, 0x70]|
|;| 0xB0|[0xd0, 0xff] |[0x20, 0x4F]|

The prefixes themselves are encoded via `!`.

Because of how the encoding above is structured, some values have more
than a single encoding, e.g.: `:~` would be `0x5f+0x7e` which is `0xdd`,
which is defined in the table as `;-`. The table represents the
canonical encoding.

Since certain encodes represent impossible values, e.g. `;~` would be
`0xB0+0x7E` which would be `0x12E` which is not 8-bits long, there are
some values that may be usful as in-band signalling. Implementations
are encouraged to provide callbacks or hooks for these to be used, but
may simply discard them.

## Example

```
==== Original as bytes====
b'This test, if you want to call it that.\xff\x7f\x01\x06\x07\x08\x00\r\n5,6,7 ,8\rIs a test of the extrema! -- and other random chars; like these: $1.40 / 1#\n'

==== Quoted (with inserted in-band signal) ====
b"This test, if you want to call it that.;O: !!!&!'!(! ;~!-!*5,6,7 ,8!-Is a test of the extrema!A -- and other random chars![ like these!Z $1.40 / 1#!*"

==== Unquoting ====
Callback with special b'~' and current output of b'This test, if you want to call it that.\xff\x7f\x01\x06\x07\x08\x00'

==== Unqoted bytes ====
b'This test, if you want to call it that.\xff\x7f\x01\x06\x07\x08\x00\r\n5,6,7 ,8\rIs a test of the extrema! -- and other random chars; like these: $1.40 / 1#\n'
```
