import sys
import json
import interpreter
import assembler


def main():
    input_file = sys.argv[1]
    binary_file = sys.argv[2]
    output_file = sys.argv[3]
    output_range = (int(sys.argv[4]), int(sys.argv[4]))

    assembler_1 = assembler.Assembler()
    assembler_1.assemble(source_file=input_file, binary_file=binary_file)

    #uvm = interpreter.UVM(memory_size=1024)
    #uvm.load_program(binary_file)
    #result = uvm.execute(output_range)

    #with open(output_file, 'w') as f:
        #json.dump(result, f, indent=4)

if __name__ == "__main__":
    main()
