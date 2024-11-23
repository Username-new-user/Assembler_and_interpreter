import assembler, interpreter, json

def test():
    assembler_1 = assembler.Assembler()
    assembler_1.assemble(source_file='test.txt', binary_file='test.bin', log_file='test_log.json')

    uvm = interpreter.UVM(memory_size=1024)
    uvm.load_program('test.bin')
    uvm.execute((1, 5), 'test_out.json')

    with open('test_out.json', 'r') as f:
        result = json.load(f)
    print(result)
    assert result == {'1': 1, '2': 1, '3': 0, '4': 1}

if __name__ == "__main__":
    test()