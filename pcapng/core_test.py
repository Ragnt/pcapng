#!/usr/bin/env python
import pcapng.linktype
import pcapng.util
import pcapng.core

def test_section_header_block():
    blk_str     = pcapng.core.section_header_block_encode()
    blk_data    = pcapng.core.section_header_block_decode(blk_str)
    pcapng.util.assert_type_str( blk_str )
    pcapng.util.assert_type_dict( blk_data )
    assert blk_data['block_type']           == 0x0A0D0D0A
    assert blk_data['block_total_len']      == 28
    assert blk_data['block_total_len']      == len( blk_str )
    assert blk_data['block_total_len']      == blk_data['block_total_len_end']
    assert blk_data['byte_order_magic']     == 0x1A2B3C4D
    assert blk_data['major_version']        == 1
    assert blk_data['minor_version']        == 0
    assert blk_data['section_len']          == -1

def test_interface_desc_block():
    blk_str    = pcapng.core.interface_desc_block_encode()
    blk_data   = pcapng.core.interface_desc_block_decode(blk_str)
    pcapng.util.assert_type_str( blk_str )
    pcapng.util.assert_type_dict( blk_data )
    assert blk_data['block_type']          == 0x00000001
    assert blk_data['block_total_len']     == 20
    assert blk_data['block_total_len']     == blk_data['block_total_len_end']
    assert blk_data['block_total_len']     == len(blk_str)
    assert blk_data['link_type']           == pcapng.linktype.LINKTYPE_ETHERNET
    assert blk_data['reserved']            == 0
    assert blk_data['snaplen']             == 0

def test_simple_pkt_block():
    blk_str   = pcapng.core.simple_pkt_block_encode('abc')
    blk_data  = pcapng.core.simple_pkt_block_decode(blk_str)
    pcapng.util.assert_type_str( blk_str )
    pcapng.util.assert_type_dict( blk_data )
    assert blk_data['block_type']           == 0x00000003
    assert blk_data['block_tot_len']        == 20
    assert blk_data['block_tot_len']        == blk_data['block_tot_len_end']
    assert blk_data['block_tot_len']        == len(blk_str)
    assert blk_data['block_tot_len']        == 16 + blk_data['pkt_data_pad_len']
    assert blk_data['original_pkt_len']     == 3
    assert blk_data['pkt_data']             == 'abc'

