import sys
import json
import assembler

class UVM:
    def __init__(self, memory_size):
        self.memory = [0] * memory_size
        self.registers = [0] * 256

    def load_program(self, binary_file):
        with open(binary_file, 'rb') as f:
            self.program = f.read()

    def execute(self, output_range):
        output = {}
        pc = 0

        while pc < len(self.program):
            instruction = self.program[pc:pc + 6]
            A = instruction[0]
            B = (instruction[1] << 8) | instruction[2]
            C = (instruction[3] << 24) | (instruction[4] << 16) | (instruction[5] << 8) | instruction[6]

            if A == 0xC0:
                self.registers[C] = B
            elif A == 0xF7:
                self.registers[B] = self.memory[self.registers[C]]
            elif A == 0x73:
                self.memory[B] = self.registers[C]
            elif A == 0x53:
                self.memory[B] = 1 if self.memory[self.registers[B]] <= self.registers[C] else 0
            
            pc += 6

        output = {f"address_{i}": self.memory[i] for i in range(output_range[0], output_range[1] + 1)}
        return output
