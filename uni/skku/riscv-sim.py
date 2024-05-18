import sys
from typing import List

"""
Constants
"""
WORD = 4
BE_FORMAT = '032b'
HEX8_FORMAT = '08x'

R_TYPE = 'R_TYPE'
I_TYPES = 'I_TYPES'
I_TYPE_ARITHMETIC = 'I_TYPE_ARITHMETIC'
I_TYPE_LOAD = 'I_TYPE_LOAD'
I_TYPE_JALR = 'I_TYPE_JALR'
S_TYPE = 'S_TYPE'
SB_TYPE = 'SB_TYPE'
U_TYPES = 'U_TYPES'
U_TYPE_LUI = 'U_TYPE_LUI'
U_TYPE_AUIPC = 'U_TYPE_AUIPC'
UJ_TYPE = 'UJ_TYPE'

opcodes = {
    R_TYPE: {'0110011'},
    I_TYPES: {'0010011', '0000011', '1100111'},
    I_TYPE_ARITHMETIC: {'0010011'},
    I_TYPE_LOAD: {'0000011'},
    I_TYPE_JALR: {'1100111'},
    S_TYPE: {'0100011'},
    SB_TYPE: {'1100011'},
    U_TYPES: {'0110111', '0010111'},
    U_TYPE_LUI: {'0110111'},
    U_TYPE_AUIPC: {'0010111'},
    UJ_TYPE: {'1101111'}
}


"""
RISCV32Simulator: simulate RISC-V instructions disassembly
"""
class RISCV32Simulator:
    def __init__(self):
        self.assembly_instructions = []

    def __str__(self):
        return '\n'.join(self.assembly_instructions)

    def proceed(self, bin_instructions: List[str]):
        IC = 0
        for instruction in bin_instructions:
            hex_code = self.bin2hex(instruction)
            assembly_instr = self.bin2assembly(instruction)
            self.assembly_instructions.append(f'inst {IC}: {hex_code} {assembly_instr}')
            IC += 1

    def bin2hex(self, bits: str) -> str:
        return format(int(bits, 2), HEX8_FORMAT)

    def bin2assembly(self, bits: str) -> str:
        opcode = bits[25:32]

        if opcode in opcodes[R_TYPE]:
            funct7 = bits[0:7]
            rs2 = bits[7:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]
            rd = bits[20:25]

            if funct3 == '000' and funct7 == '0000000':
                return f'add x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == "000" and funct7 == '0100000':
                return f'sub x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == '001' and funct7 == '0000000':
                return f'sll x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == '010' and funct7 == '0000000':
                return f'slt x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == '011' and funct7 == '0000000':
                return f'sltu x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == "100" and funct7 == '0000000':
                return f'xor x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == '101' and funct7 == '0000000':
                return f'srl x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == '101' and funct7 == '0100000':
                return f'sra x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == '110' and funct7 == '0000000':
                return f'or x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'
            elif funct3 == '111' and funct7 == '0000000':
                return f'and x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}'

        elif opcode in opcodes[I_TYPES]:
            imm = bits[0:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]
            rd = bits[20:25]

            if opcode in opcodes[I_TYPE_ARITHMETIC]:
                if funct3 == '000':
                    return f'addi x{int(rd, 2)}, x{int(rs1, 2)}, {self.imm2dec(imm)}'
                elif funct3 == '010':
                    return f'slti x{int(rd, 2)}, x{int(rs1, 2)}, {self.imm2dec(imm)}'
                elif funct3 == '011':
                    return f'sltiu x{int(rd, 2)}, x{int(rs1, 2)}, {self.imm2dec(imm)}'
                elif funct3 == '100':
                    return f'xori x{int(rd, 2)}, x{int(rs1, 2)}, {self.imm2dec(imm)}'
                elif funct3 == '110':
                    return f'ori x{int(rd, 2)}, x{int(rs1, 2)}, {self.imm2dec(imm)}'
                elif funct3 == '111':
                    return f'andi x{int(rd, 2)}, x{int(rs1, 2)}, {self.imm2dec(imm)}'
                elif funct3 == '001' and imm[0:7] == '0000000':
                    return f'slli x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm[7:], 2)}'
                elif funct3 == "101" and imm[0:7] == '0000000':
                    return f'srli x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm[7:], 2)}'
                elif funct3 == '101' and imm[0:7] == '0100000':
                    return f'srai x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm[7:], 2)}'

            elif opcode in opcodes[I_TYPE_LOAD]:
                if funct3 == '000':
                    return f'lb x{int(rd, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'
                elif funct3 == '001':
                    return f'lh x{int(rd, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'
                elif funct3 == '010':
                    return f'lw x{int(rd, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'
                elif funct3 == '100':
                    return f'lbu x{int(rd, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'
                elif funct3 == '101':
                    return f'lhu x{int(rd, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'

            elif opcode in opcodes[I_TYPE_JALR] and funct3 == '000':
                return f'jalr x{int(rd, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'

        elif opcode in opcodes[S_TYPE]:
            imm = bits[0:7] + bits[20:25]
            rs2 = bits[7:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]

            if funct3 == '000':
                return f'sb x{int(rs2, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'
            elif funct3 == '001':
                return f'sh x{int(rs2, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'
            elif funct3 == '010':
                return f'sw x{int(rs2, 2)}, {self.imm2dec(imm)}(x{int(rs1, 2)})'

        elif opcode in opcodes[SB_TYPE]:
            imm = bits[0] + bits[24] + bits[1:7] + bits[20:24] + '0'
            rs2 = bits[7:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]

            if funct3 == '000':
                return f'beq x{int(rs1, 2)}, x{int(rs2, 2)}, {self.imm2dec(imm)}'
            elif funct3 == '001':
                return f'bne x{int(rs1, 2)}, x{int(rs2, 2)}, {self.imm2dec(imm)}'
            elif funct3 == '100':
                return f'blt x{int(rs1, 2)}, x{int(rs2, 2)}, {self.imm2dec(imm)}'
            elif funct3 == '101':
                return f'bge x{int(rs1, 2)}, x{int(rs2, 2)}, {self.imm2dec(imm)}'
            elif funct3 == '110':
                return f'bltu x{int(rs1, 2)}, x{int(rs2, 2)}, {self.imm2dec(imm)}'
            elif funct3 == '111':
                return f'bgeu x{int(rs1, 2)}, x{int(rs2, 2)}, {self.imm2dec(imm)}'

        elif opcode in opcodes[U_TYPES]:
            imm = bits[0:20] + '000000000000'
            rd = bits[20:25]

            if opcode in opcodes[U_TYPE_LUI]:
                return f'lui x{int(rd, 2)}, {self.imm2dec(imm)}'
            elif opcode in opcodes[U_TYPE_AUIPC]:
                return f'auipc x{int(rd, 2)}, {self.imm2dec(imm)}'

        elif opcode in opcodes[UJ_TYPE]:
            imm = (bits[0] + bits[12:20] + bits[11] + bits[1:11] + '0')
            rd = bits[20:25]
            return f'jal x{int(rd, 2)}, {self.imm2dec(imm)}'

        return 'unknown instruction'

    def imm2dec(self, bits: str) -> int:
        if bits[0] == '1':
            return -(int(''.join(['1' if bit == '0' else '0' for bit in bits[1:]]), 2) + 1)
        else:
            return int(bits, 2)

    def clear(self):
        self.assembly_instructions = []


"""
Read file with binary code and split it into 32-bit instructions, each converted to BigEndian format
"""
def try_read_binary_data(filename: str):
    try:
        data = []
        with open(filename, 'rb') as f:
            while True:
                binary_le = f.read(WORD)
                if not binary_le:
                    break

                decimal = int.from_bytes(binary_le, byteorder='little', signed=False)
                binary_be = format(decimal, BE_FORMAT)
                data.append(binary_be)
        return data

    except Exception:
        return None


"""
Main: read data from binary file and use `RISCV32Simulator` to dissemble it
"""
if __name__ == "__main__":
    file = sys.argv[1]
    if file is None or file == '':
        print('Error: no input file provided! Exiting...')
        sys.exit(1)

    data = try_read_binary_data(file)
    if data is not None:
        simulator = RISCV32Simulator()
        simulator.proceed(data)
        print(simulator)
        simulator.clear()
    else:
        print('Error: could not read binary data from file! Exiting...')
