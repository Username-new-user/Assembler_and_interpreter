import sys
import json
import interpreter


def main():
    binary_file = sys.argv[1]
    output_file = sys.argv[2]
    output_range = (int(sys.argv[3]), int(sys.argv[4]))

    uvm = interpreter.UVM(memory_size=1024)  # Пример размера памяти
    uvm.load_program(binary_file)
    result = uvm.execute(output_range)

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    main()
