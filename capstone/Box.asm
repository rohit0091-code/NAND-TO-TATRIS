// Box.asm
// Student: Rohit Sharma | Roll No: 2501730345 | K = 45
// Box Specifications:
//   Starting Row = K = 45 (Offset = 32 * 45 = 1440; Start Address = 16384 + 1440 = 17824)
//   Height       = 20 rows (rows 45 to 64)
//   Width        = 16 * ((45 mod 4) + 1) = 16 * 2 = 32 pixels (2 consecutive 16-bit words per row)
//   Behavior     = Draws black box (-1) while any key is pressed; erases box (0) when key is released.

(LOOP)
    // Read keyboard memory (RAM[24576])
    @KBD
    D=M

    // If KBD == 0, no key is pressed -> set fill color = 0 (white)
    @SET_WHITE
    D;JEQ

    // Otherwise, a key is pressed -> set fill color = -1 (black: 1111111111111111)
    @color
    M=-1
    @START_DRAW
    0;JMP

(SET_WHITE)
    @color
    M=0

(START_DRAW)
    // Calculate starting address: SCREEN (16384) + 1440 (row 45)
    @SCREEN
    D=A
    @1440
    D=D+A
    @addr
    M=D

    // Initialize row counter = 20
    @20
    D=A
    @rows
    M=D

(DRAW_ROW)
    // Check if all 20 rows have been processed
    @rows
    D=M
    @LOOP
    D;JEQ

    // Draw Word 0 (pixels 0..15 from left edge)
    @color
    D=M
    @addr
    A=M
    M=D

    // Draw Word 1 (pixels 16..31 from left edge -> 32 pixels total width)
    @color
    D=M
    @addr
    A=M+1
    M=D

    // Advance addr by 32 words to reach the same column in the next row
    @32
    D=A
    @addr
    M=M+D

    // Decrement remaining row count
    @rows
    M=M-1

    // Repeat for next row
    @DRAW_ROW
    0;JMP
