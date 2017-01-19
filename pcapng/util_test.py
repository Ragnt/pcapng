#!/usr/bin/env python
import struct
import time
import pytest
import pcapng.util

def test_block32_pad_len():
    assert 0 == pcapng.util.block32_pad_len(  0 )

    assert 4 == pcapng.util.block32_pad_len(  1 )
    assert 4 == pcapng.util.block32_pad_len(  2 )
    assert 4 == pcapng.util.block32_pad_len(  3 )
    assert 4 == pcapng.util.block32_pad_len(  4 )

    assert 8 == pcapng.util.block32_pad_len(  5 )
    assert 8 == pcapng.util.block32_pad_len(  6 )
    assert 8 == pcapng.util.block32_pad_len(  7 )
    assert 8 == pcapng.util.block32_pad_len(  8 )

def test_pad_to_len():
    with pytest.raises(AssertionError): pcapng.util.pad_to_len( [1, 2, 3, 4], 3 )
    with pytest.raises(AssertionError): pcapng.util.pad_to_len( 5, 3 )

    assert [0, 0, 0, 0] == pcapng.util.pad_to_len( [          ], 4 )
    assert [1, 0, 0, 0] == pcapng.util.pad_to_len( [1,        ], 4 )
    assert [1, 2, 0, 0] == pcapng.util.pad_to_len( [1, 2      ], 4 )
    assert [1, 2, 3, 0] == pcapng.util.pad_to_len( [1, 2, 3   ], 4 )
    assert [1, 2, 3, 4] == pcapng.util.pad_to_len( [1, 2, 3, 4], 4 )

    assert [9, 9, 9, 9] == pcapng.util.pad_to_len( [          ], 4, 9)
    assert [1, 9, 9, 9] == pcapng.util.pad_to_len( [1,        ], 4, 9)
    assert [1, 2, 9, 9] == pcapng.util.pad_to_len( [1, 2      ], 4, 9)
    assert [1, 2, 3, 9] == pcapng.util.pad_to_len( [1, 2, 3   ], 4, 9)
    assert [1, 2, 3, 4] == pcapng.util.pad_to_len( [1, 2, 3, 4], 4, 9)

def test_pad_to_block32():
    assert [                      ] == pcapng.util.pad_to_block32( [                      ] )
    assert [1, 0, 0, 0            ] == pcapng.util.pad_to_block32( [1                     ] )
    assert [1, 2, 0, 0            ] == pcapng.util.pad_to_block32( [1, 2                  ] )
    assert [1, 2, 3, 0            ] == pcapng.util.pad_to_block32( [1, 2, 3               ] )
    assert [1, 2, 3, 4            ] == pcapng.util.pad_to_block32( [1, 2, 3, 4            ] )
    assert [1, 2, 3, 4, 5, 0, 0, 0] == pcapng.util.pad_to_block32( [1, 2, 3, 4, 5         ] )
    assert [1, 2, 3, 4, 5, 6, 0, 0] == pcapng.util.pad_to_block32( [1, 2, 3, 4, 5, 6      ] )
    assert [1, 2, 3, 4, 5, 6, 7, 0] == pcapng.util.pad_to_block32( [1, 2, 3, 4, 5, 6, 7   ] )
    assert [1, 2, 3, 4, 5, 6, 7, 8] == pcapng.util.pad_to_block32( [1, 2, 3, 4, 5, 6, 7, 8] )

    pcapng.util.assert_block32_size( [                      ] )
    pcapng.util.assert_block32_size( [1, 2, 3, 4            ] )
    pcapng.util.assert_block32_size( [1, 2, 3, 4, 5, 6, 7, 8] )
    with pytest.raises(AssertionError): pcapng.util.assert_block32_size( [1        ] )
    with pytest.raises(AssertionError): pcapng.util.assert_block32_size( [1, 2     ] )
    with pytest.raises(AssertionError): pcapng.util.assert_block32_size( [1, 2, 3  ] )


def test_xxx():
    xx1 = struct.pack(   '!hhl', 1, 2, 3 )  # h='short', l='long'
    xx2 = struct.unpack( '!hhl', xx1 )      # ! => network byte order (big-endian)
    assert xx1 == '\x00\x01\x00\x02\x00\x00\x00\x03'
    assert xx2 == ( 1, 2, 3 )
    assert '\x00\x00\x00\x00\x00\x00\x00\x05' == struct.pack( '!q', 5 )
    assert '\x00\x00\x00\x05'                 == struct.pack( '!l', 5 )
    assert '\x00\x05'                         == struct.pack( '!h', 5 )
    assert 1 == pcapng.util.first( [1,2,3] )

    assert 3 == len( [ 1, 2, 3] )
    assert (3, 140000) == pcapng.util.split_float(3.14)
    assert (3, 141593) == pcapng.util.split_float(3.141592654)

    assert [97, 98, 99]      == pcapng.util.str_to_ByteList('abc')
    assert ['a', 'b', 'c']   == pcapng.util.ByteList_to_ChrList([97, 98, 99])
    assert 'abc'             == pcapng.util.ByteList_to_str([97, 98, 99])
    assert 'abc'             == pcapng.util.ChrList_to_str(['a', 'b', 'c'])

    ts1 = pcapng.util.curr_utc_time_tuple()
    time.sleep(0.1)
    delta = pcapng.util.timetup_subtract( ts1, pcapng.util.curr_utc_time_tuple() )
    assert ((0.09 < delta) and (delta < 0.11))
