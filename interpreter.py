import sys
import json
import assembler

class UVM:
    def __init__(self, memory_size):
        self.memory = [0] * memory_size
        self.registers = [0] * 256  # 256 регистров

    def load_program(self, binary_file):
        with open(binary_file, 'rb') as f:
            self.program = f.read()

    def execute(self, output_range):
        output = {}
        pc = 0  # счетчик команд

        while pc < len(self.program):
            instruction = self.program[pc:pc + 6]
            A = instruction[0]
            B = (instruction[1] << 8) | instruction[2]
            C = (instruction[3] << 24) | (instruction[4] << 16) | (instruction[5] << 8) | instruction[6]

            if A == 0xC0:  # LOAD_CONST
                self.registers[C] = B
            elif A == 0xF7:  # READ_MEM
                self.registers[B] = self.memory[self.registers[C]]
            elif A == 0x73:  # WRITE_MEM
                self.memory[B] = self.registers[C]
            elif A == 0x53:  # BINARY_OP_LEQ
                self.memory[B] = 1 if self.memory[self.registers[B]] <= self.registers[C] else 0
            
            pc += 6

        # Сохранение результата
        # Сохранение результата в формате JSON
        output = {f"address_{i}": self.memory[i] for i in range(output_range[0], output_range[1] + 1)}
        return output
