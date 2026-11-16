#!/usr/bin/env python3
"""Check address/data equivalence, vectors, SWD symbols and the persistence boundary."""
from pathlib import Path
from hashlib import sha256
import struct
import sys
from elftools.elf.elffile import ELFFile
from intelhex import IntelHex

def main(elf_name, hex_name):
    image = IntelHex(hex_name)
    hex_data = {address: image[address] for address in image.addresses()}
    with open(elf_name, 'rb') as source:
        elf = ELFFile(source)
        assert elf.header['e_machine'] == 'EM_ARM' and elf.elfclass == 32 and elf.little_endian
        load = {}
        segments = [s for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD' and s['p_filesz']]
        # objcopy emits allocated section bytes, omitting uninitialized/TLS and alignment
        # holes. Match each initialized section to its segment's load (physical) address.
        for section in elf.iter_sections():
            if not section['sh_flags'] & 2 or section['sh_type'] == 'SHT_NOBITS' or not section['sh_size']:
                continue
            matches = [s for s in segments if s.section_in_segment(section)]
            assert len(matches) == 1, f'ambiguous load mapping: {section.name}'
            segment = matches[0]
            base = segment['p_paddr'] + section['sh_addr'] - segment['p_vaddr']
            for i, byte in enumerate(section.data()):
                assert base+i not in load, f'overlapping sections: {section.name}'
                load[base+i] = byte
        assert load == hex_data, 'initialized ELF section bytes or address set differ from HEX'
        assert min(load) == 0 and max(load) < 0x15d000, 'image touches persistent panel journal'
        msp, reset_vector = struct.unpack('<II',bytes(load[i] for i in range(8)))
        assert 0x20000000 < msp <= 0x2002f000 and msp % 8 == 0
        assert reset_vector & 1 and (reset_vector & ~1) in load, 'invalid Thumb reset vector'
        symbols = {s.name:s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols()}
        for name in ('astra_report','astra_time_mailbox','astra_fixture_hook','astra_done_hook','choose_refresh','render_frame','main'):
            assert name in symbols
        print(f'PASS ARM ELF32 little-endian, initial MSP=0x{msp:08x}, Thumb reset=0x{reset_vector:08x}')
        print(f'PASS {len(load)} initialized bytes identical at every ELF/HEX load address')
        print(f'PASS max programmed address=0x{max(load):08x}; journal 0x15d000..0x164fff untouched')
        for name in ('astra_report','astra_time_mailbox','astra_fixture_hook','astra_done_hook','choose_refresh','render_frame'):
            print(f'{name} = 0x{symbols[name]:08x}')
    for name in (elf_name,hex_name):
        print(f'{sha256(Path(name).read_bytes()).hexdigest()}  {Path(name).name}')

if __name__=='__main__':
    main(*sys.argv[1:])
