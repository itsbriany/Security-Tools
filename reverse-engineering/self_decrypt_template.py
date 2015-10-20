# An instrumentation script template that tricks the software into decrypting
# data that it previously encrypted

# Dependencies: Immunity Debugger

# Author: Brian Yip


import immlib

def main(args):
    imm = immlib.Debugger()

    encrypted_file = open('''Path to encrypted file''', "rb")

    in_file = encrypted_file.read()
    in_buffer_size = len(in_file)

    # Allocate memory in the debugged process and write the data
    # from the encrypted file into it
    remote_in_buffer = imm.remoteVirtualAlloc(in_buffer_size)
    imm.writeMemory(in_file, remote_in_buffer)
    encrypted_file.close()

    decrypted_file = open('''Path to where to write decrypted file''', "w")

    # Change this to suit your needs
    imm.setReg("EIP", 0xdeadbeef)
    imm.setBreakpoint(0x01234567)
    imm.run()


    # Modify registers once breakpoint is reached
    # Example: Set the second argument to the length of the encrypted file
    # as the second argument and remote_in_buffer as the first argument
    regs = imm.getRegs()
    imm.writeLong(regs["EBP"] + 0xC, in_buffer_size)
    imm.writeLong(regs["EBP"] + 0x8, remote_in_buffer)

    # Set a breakpoint to pause execution and fetch the decrypted contents
    imm.setBreakpoint(0x11111111)
    imm.run()

    results = imm.readMemory(remote_in_buffer, in_buffer_size)
    decrypted_file.write(results)
    decrypted_file.close()

