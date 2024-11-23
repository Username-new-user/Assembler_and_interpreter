import json
from bitarray import bitarray

def to_binary(number):
    return bin(number)[2:]

def to_hex(number):
    return hex(number)[2:]

def from_binary(binary):
    return int(binary, 2)

COMMANDS = {
            'LOAD_CONST': 0xC0,
            'READ_MEM': 0xF7,
            'WRITE_MEM': 0x73,
            'BINARY_OP_LEQ': 0x53,
        }

class Assembler():

    log = {}

    def assemble_line(self, line: str):
        parts = line.split()
        command = parts[0]
        if command not in COMMANDS:
            raise ValueError(f"Unknown command: {command}")
        
        A = COMMANDS[command]
        B = int(parts[1])
        C = int(parts[2])
        size = 48

        bit_arr = bitarray(endian='big')

        if command == 'LOAD_CONST':
            packed_data = (A << (size - 8)) | (B << (size - 34)) | (C << (size - 41))
            bit_arr.frombytes(packed_data.to_bytes(6, byteorder='big'))

        elif command == 'READ_MEM':
            packed_data = (A << (size - 8)) | (B << (size - 15)) | (C << (size - 22))
            bit_arr.frombytes(packed_data.to_bytes(6, byteorder='big'))
        elif command == 'WRITE_MEM':
            packed_data = (A << (size - 8)) | (B << (size - 35)) | (C << (size - 42))
            bit_arr.frombytes(packed_data.to_bytes(6, byteorder='big'))
        elif command == 'BINARY_OP_LEQ':
            packed_data = (A << (size - 8)) | (B << (size - 15)) | (C << (size - 22))
            bit_arr.frombytes(packed_data.to_bytes(6, byteorder='big'))
        else:
            raise ValueError(f"Unknown command: {command}")
        self.log[len(self.log)] = [command, B, C]
        return bit_arr

        
    def assemble(self, source_file: str, binary_file: str, log_file: str):
        with open(source_file, 'r') as f:
            lines = f.readlines()
        with open(binary_file, 'wb') as f:
            for line in lines:
                f.write(self.assemble_line(line))
        
        with open(log_file, 'w') as f:
            json.dump(self.log, f, indent=4)