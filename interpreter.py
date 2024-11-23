import json
from bitarray import bitarray

class UVM:
    def __init__(self, memory_size):
        self.memory = [0] * memory_size
        self.registers = [0] * 1024

    def load_program(self, binary_file):
        with open(binary_file, 'rb') as f:
            self.program = f.read()

    def load_const(self, B, C):
        self.registers[B] = C

    def read_mem(self, B, C):
        self.registers[B] = self.memory[C]

    def write_mem(self, B, C):
        self.memory[B] = self.registers[C]

    def binary_op_leq(self, B, C):
        self.registers[B] = self.registers[B] <= self.registers[C]

    def execute(self, output_range, output_file):
        output = {}
        pc = 0
        while pc < len(self.program):
            instruction = self.program[pc:pc + 6]
            A = instruction[0]
            bit_array = bitarray(endian='big')
            bit_array.frombytes(instruction)

            match A:
                case 192:
                    B = int(bit_array[8:34].to01(), 2)
                    C = int(bit_array[34:41].to01(), 2)
                    self.load_const(B, C)
                case 247:
                    B = int(bit_array[8:15].to01(), 2)
                    C = int(bit_array[15:22].to01(), 2)
                    self.read_mem(B, C)
                case 115:
                    B = int(bit_array[8:35].to01(), 2)
                    C = int(bit_array[35:42].to01(), 2)
                    self.write_mem(B, C)
                case 83:
                    B = int(bit_array[8:15].to01(), 2)
                    C = int(bit_array[15:22].to01(), 2)
                    self.binary_op_leq(B, C)
            pc += 6

        for i in range(*output_range):
            output[i] = self.memory[i]

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=4)
        return output
