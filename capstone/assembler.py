#!/usr/bin/env python3
"""
Two-Pass Hack Assembler
Student: Rohit Sharma
Roll No: 2501730345
Personal Number (K): 45
Additional Feature (K mod 3 = 0): Save all labels and variables with their addresses in "symbols.txt"
"""

import sys
import os


class HackAssembler:
    def __init__(self):
        # Predefined Hack symbols
        self.symbol_table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        for i in range(16):
            self.symbol_table[f"R{i}"] = i

        # Track labels and variables separately for clean symbols.txt reporting
        self.labels = {}
        self.variables = {}
        self.next_ram_address = 16

        # Computation mnemonic lookup table (a + c1..c6)
        self.comp_table = {
            "0":   "0101010",
            "1":   "0111111",
            "-1":  "0111010",
            "D":   "0001100",
            "A":   "0110000",
            "!D":  "0001101",
            "!A":  "0110001",
            "-D":  "0001111",
            "-A":  "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "A+D": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "A&D": "0000000",
            "D|A": "0010101",
            "A|D": "0010101",
            "M":   "1110000",
            "!M":  "1110001",
            "-M":  "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "M+D": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "M&D": "1000000",
            "D|M": "1010101",
            "M|D": "1010101",
        }

        # Destination mnemonic lookup table (d1 d2 d3)
        self.dest_table = {
            "":    "000",
            "M":   "001",
            "D":   "010",
            "MD":  "011",
            "DM":  "011",
            "A":   "100",
            "AM":  "101",
            "MA":  "101",
            "AD":  "110",
            "DA":  "110",
            "AMD": "111",
            "ADM": "111",
            "MAD": "111",
            "MDA": "111",
            "DAM": "111",
            "DMA": "111",
        }

        # Jump mnemonic lookup table (j1 j2 j3)
        self.jump_table = {
            "":    "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }

    def clean_lines(self, raw_lines):
        """Remove comments (//...) and whitespace/blank lines."""
        cleaned = []
        for line in raw_lines:
            # Strip inline comments
            comment_idx = line.find("//")
            if comment_idx != -1:
                line = line[:comment_idx]
            line = line.strip()
            if line:
                cleaned.append(line)
        return cleaned

    def first_pass(self, lines):
        """Record (LABEL) declarations and their ROM instruction addresses."""
        instructions = []
        rom_address = 0
        for line in lines:
            if line.startswith("(") and line.endswith(")"):
                label = line[1:-1].strip()
                if label not in self.symbol_table:
                    self.symbol_table[label] = rom_address
                    self.labels[label] = rom_address
            else:
                instructions.append(line)
                rom_address += 1
        return instructions

    def translate_a_instruction(self, instruction):
        """Convert @value or @symbol to 16-bit binary string."""
        symbol = instruction[1:].strip()
        if symbol.isdigit():
            address = int(symbol)
        else:
            if symbol not in self.symbol_table:
                self.symbol_table[symbol] = self.next_ram_address
                self.variables[symbol] = self.next_ram_address
                self.next_ram_address += 1
            address = self.symbol_table[symbol]
        return f"0{address:015b}"

    def translate_c_instruction(self, instruction):
        """Convert dest=comp;jump to 16-bit binary string."""
        dest_part = ""
        jump_part = ""
        comp_part = instruction

        if "=" in comp_part:
            dest_part, comp_part = comp_part.split("=", 1)
            dest_part = dest_part.strip()

        if ";" in comp_part:
            comp_part, jump_part = comp_part.split(";", 1)
            jump_part = jump_part.strip()

        comp_part = comp_part.replace(" ", "")

        if comp_part not in self.comp_table:
            raise ValueError(f"Invalid comp mnemonic: '{comp_part}'")
        if dest_part not in self.dest_table:
            raise ValueError(f"Invalid dest mnemonic: '{dest_part}'")
        if jump_part not in self.jump_table:
            raise ValueError(f"Invalid jump mnemonic: '{jump_part}'")

        return (
            "111"
            + self.comp_table[comp_part]
            + self.dest_table[dest_part]
            + self.jump_table[jump_part]
        )

    def second_pass(self, instructions):
        """Convert all instructions to 16-bit binary machine code."""
        machine_code = []
        for inst in instructions:
            if inst.startswith("@"):
                machine_code.append(self.translate_a_instruction(inst))
            else:
                machine_code.append(self.translate_c_instruction(inst))
        return machine_code

    def save_symbols(self, output_dir="."):
        """
        Additional Feature (K = 45, 45 mod 3 = 0):
        Save all labels and variables with their addresses in 'symbols.txt'.
        """
        symbols_path = os.path.join(output_dir, "symbols.txt")
        with open(symbols_path, "w", encoding="utf-8") as f:
            f.write("=== HACK ASSEMBLER SYMBOL TABLE (K = 45, K mod 3 = 0) ===\n\n")
            f.write("--- LABELS (ROM Addresses) ---\n")
            if self.labels:
                for label, addr in self.labels.items():
                    f.write(f"{label:<20} : {addr}\n")
            else:
                f.write("(None)\n")

            f.write("\n--- VARIABLES (RAM Addresses starting at 16) ---\n")
            if self.variables:
                for var, addr in self.variables.items():
                    f.write(f"{var:<20} : {addr}\n")
            else:
                f.write("(None)\n")

            f.write("\n--- PREDEFINED SYMBOLS ---\n")
            for sym, addr in self.symbol_table.items():
                if sym not in self.labels and sym not in self.variables:
                    f.write(f"{sym:<20} : {addr}\n")
        return symbols_path

    def assemble_file(self, asm_path):
        if not os.path.isfile(asm_path):
            raise FileNotFoundError(f"Assembly file not found: {asm_path}")

        with open(asm_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        cleaned = self.clean_lines(raw_lines)
        instructions = self.first_pass(cleaned)
        binary_lines = self.second_pass(instructions)

        base_name = os.path.splitext(asm_path)[0]
        hack_path = base_name + ".hack"
        with open(hack_path, "w", encoding="utf-8") as f:
            for code in binary_lines:
                f.write(code + "\n")

        out_dir = os.path.dirname(os.path.abspath(asm_path))
        symbols_path = self.save_symbols(out_dir)
        return hack_path, symbols_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <Program.asm>")
        sys.exit(1)

    asm_file = sys.argv[1]
    assembler = HackAssembler()
    hack_file, sym_file = assembler.assemble_file(asm_file)
    print(f"Successfully assembled '{asm_file}' -> '{hack_file}'")
    print(f"Saved symbol table -> '{sym_file}'")


if __name__ == "__main__":
    main()
