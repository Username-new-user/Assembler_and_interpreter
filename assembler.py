import struct

COMMANDS = {
            'LOAD_CONST': 0xC0,
            'READ_MEM': 0xF7,
            'WRITE_MEM': 0x73,
            'BINARY_OP_LEQ': 0x53,
        }

class Assembler():
    def assemble_line(self, line: str):
        parts = line.split()
        command = parts[0]
        if command not in COMMANDS:
            raise ValueError(f"Unknown command: {command}")
        
        A = COMMANDS[command]
        B = int(parts[1])
        C = int(parts[2])
        
        if command == 'LOAD_CONST':
        # Упаковка данных с использованием struct.pack
            return struct.pack('<BIB', A, B, C)
        elif command == 'READ_MEM':
            return struct.pack('<BBB', A, B, C) + struct.pack('<BH', 0, 0)  # 3 байта для заполнения
        elif command == 'WRITE_MEM':
            return struct.pack('<H', 247) + struct.pack('<H', B) + struct.pack('<2H', C)
        elif command == 'BINARY_OP_LEQ':
            return struct.pack('<BBH', A, (B >> 8) & 0xFF, B & 0xFF) + struct.pack('<B', 0x00)  # 1 байт для заполнения

assembler = Assembler()
line = str('LOAD_CONST 462 64')
print(assembler.assemble_line(line=line))
line = str('READ_MEM 15 3')
print(assembler.assemble_line(line=line))
line = str('WRITE_MEM 633 127')
print(assembler.assemble_line(line=line))
line = str('BINARY_OP_LEQ 40 114')
print(assembler.assemble_line(line=line))

