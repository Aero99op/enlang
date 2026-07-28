"""Dead Code Elimination Optimizer for EnLang IR."""
from ..ir.ir_nodes import IRBlock, IRInstruction

class DeadCodeEliminator:
    """Removes unreachable instructions after unconditional return jumps."""
    @classmethod
    def eliminate_block(cls, ir_block):
        new_instrs = []
        terminated = False
        for instr in ir_block.instructions:
            if terminated:
                break
            new_instrs.append(instr)
            if instr.op in ('RET', 'JUMP'):
                terminated = True
        ir_block.instructions = new_instrs
        return ir_block
