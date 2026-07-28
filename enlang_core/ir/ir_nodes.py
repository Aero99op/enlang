"""Backend-Agnostic Intermediate Representation (IR) Instruction Nodes."""

class IRInstruction:
    """Base class for all EnLang IR instructions."""
    def __init__(self, op, dest=None, arg1=None, arg2=None):
        self.op = op          # e.g., 'LOAD_VAL', 'ADD', 'STORE', 'CALL', 'LABEL', 'JUMP', 'JUMP_IF_FALSE'
        self.dest = dest      # Target register or symbol
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        parts = [self.op]
        if self.dest is not None:
            parts.append(f"dest={self.dest}")
        if self.arg1 is not None:
            parts.append(f"arg1={self.arg1}")
        if self.arg2 is not None:
            parts.append(f"arg2={self.arg2}")
        return f"IRInstruction({', '.join(parts)})"

class IRBlock:
    """A basic block of sequential IR instructions."""
    def __init__(self, label=None):
        self.label = label
        self.instructions = []

    def append(self, instr):
        self.instructions.append(instr)

class IRFunction:
    """IR representation of a function containing basic blocks."""
    def __init__(self, name, params=None):
        self.name = name
        self.params = params or []
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)
