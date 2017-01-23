import struct
import sys
import time
import math

# Global var's
test_ctx = {
    'enable'    : False,
    'utc_secs'  : -1.2      # floating point unix time
}
def set_test_time_utc( utc_secs ):
    global test_ctx
    test_ctx['enable']      = True
    test_ctx['utc_time']    = utc_secs

#-----------------------------------------------------------------------------

def is_python2():
    (major, minor, micro, release_level, serial) = sys.version_info
    return ((major == 2) and (minor == 7))

def is_python3():
    (major, minor, micro, release_level, serial) = sys.version_info
    return ((major == 3) and (minor >= 5))

def assert_python2():
    assert is_python2()


def assert_type_bytearray( arg ):
    assert type( arg ) == bytearray

def assert_type_bytes( arg ):
    assert type( arg ) == bytes

def assert_type_str( arg ):
    assert type( arg ) == str

def assert_type_list( arg ):
    assert type( arg ) == list

def assert_type_dict( arg ):
    assert type( arg ) == dict

def assert_uint8(arg):        # unsigned byte
    assert (0 <= arg <= 255)

def assert_int8(arg):          # signed byte
    assert (-128 <= arg <= 127)


def to_bytes( arg ):
    """Converts arg to a 'bytes' object."""
    return bytes( bytearray( arg ))    # if python2, 'bytes' is synonym for 'str'

def str_to_bytes( arg ):
    """Converts a string arg to a 'bytes' object."""
    assert_type_str( arg )
    """Convert an ASCII string to 'bytes'. Works on both Python2 and Python3."""
    return to_bytes( map(ord,arg))


#todo move to pcap
def fmt_pcap_hdr( ts_sec, ts_usec, incl_len, orig_len ):
    """Format a PCAP block header."""
    packed = struct.pack( '>LLLL', ts_sec, ts_usec, incl_len, orig_len)
    return packed


def split_float( fval ):
    """Splits a float into integer and fractional parts."""
    frac, whole = math.modf( fval )
    micros = int( round( frac * 1000000 ))
    return int(whole), micros

def curr_utc_timetuple():
    """Returns the current UTC time as a (secs, usecs) tuple."""
    global test_ctx
    if test_ctx['enable']:
        utc_secs = test_ctx['utc_time']
    else:
        utc_secs = time.time()
    secs, usecs = split_float( utc_secs )
    return secs, usecs

def curr_utc_secs():
    """Returns the current UTC time in integer seconds."""
    secs, usecs = curr_utc_timetuple()
    return secs

def timeTuple_to_float(secs, usecs):
    """Converts a time tuple from (secs, usecs) to float."""
    return secs + (usecs / 1000000.0)

def timeTuple_subtract(ts1, ts2):
    """Subtracts two time tuples in (secs, usecs) format, returning a float result."""
    (s1, us1) = ts1
    (s2, us2) = ts2
    t1 = timeTuple_to_float(s1, us1)
    t2 = timeTuple_to_float(s2, us2)
    delta = t2 - t1
    return delta

def chrList_to_str(arg):
    """ Convert a list of characters to a string"""
    #todo verify input type & values [0..255]
    strval = ''.join( arg )
    return strval

#todo move to pcapng.list (or delete?); only(), second(), last(), butlast(), rest()
def first( lst ):
    """Returns the first item in a sequence."""
    return lst[0]

#todo move to pcapng.types ?
#-----------------------------------------------------------------------------
def ipAddr_encode( ip_vals ):
    assert 4 == len( ip_vals )
    ip_bytes = struct.pack( '!BBBB', *ip_vals )
    return ip_bytes

def ipAddr_decode( ip_bytes ):
    assert 4 == len( ip_bytes )
    ip_vals = list( struct.unpack( '!BBBB',  ip_bytes ))
    return ip_vals

#todo move to pcapng.bytes
#-----------------------------------------------------------------------------

def block32_ceil_bytes(curr_len):
    """Returns the number of bytes (n >= curr_len) at the next 32-bit boundary"""
    curr_blks = float(curr_len) / 4.0
    pad_blks = int( math.ceil( curr_blks ))
    padded_len = pad_blks * 4
    return padded_len

def pad_bytes(data, tgt_length, padval=0):
    """Add (n>=0) 'padval' bytes to extend data to tgt_length"""
    elem_needed = tgt_length - len(data)
    assert (elem_needed >= 0), "padding cannot be negative"
    result = to_bytes(data) + to_bytes( [padval] )*elem_needed
    return result

def block32_pad_bytes(data):
    """Pad data with (n>=0) 0x00 bytes to reach the next 32-bit boundary"""
    padded_len = block32_ceil_bytes(len(data))
    result = pad_bytes(data, padded_len)
    return result

def assert_block32_length(data):
    """Assert that data length is at a 32-bit boundary"""
    assert (0 == len(data) % 4), "data must be 32-bit aligned"
    return True

#todo add a "custom bytes" header tag? if so, verify on unpack
def block32_bytes_pack(data_bytes):
    data_bytes = to_bytes( data_bytes )
    data_bytes_len = len( data_bytes )
    packed_bytes = struct.pack('!L', data_bytes_len) + block32_pad_bytes(data_bytes)
    return packed_bytes

def block32_bytes_unpack(packed_bytes):
    (data_bytes_len,) = struct.unpack( '!L', packed_bytes[:4] )
    data_bytes_pad = packed_bytes[4:]
    data_bytes = data_bytes_pad[:data_bytes_len]
    return data_bytes


