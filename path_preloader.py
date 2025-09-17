from pathlib import Path
from os import makedirs
from sys import exit

normal_file_size = 4 * 1024 * 1024
name_dir = Path("preloader_path/boot1.bin")
print("Dev. Max_Goblin - 4pda")

def auto_path_preloader(flag: bytes, fastboot_lock_state: int, file_size: int):
    with open(Path("preloader_path/boot1.bin"), "r+b") as f:
        # read code offset
        f.seek(0x20d)
        code_offset = f.read(0x1)[0] * 256
        f.seek(0x21d)
        code_offset1 = f.read(0x1)
        f.seek(0x211)
        code_offset2 = f.read(0x1)
        f.seek(0x212)
        code_offset3 = f.read(0x1)
        f.seek(0x221)
        code_offset4 = f.read(0x1)
        f.seek(0x222)
        code_offset5 = f.read(0x1)

        # read code 
        f.seek(code_offset)
        jumpr = f.read(file_size - 0x11120)

        # writing zeros
        print(f"Write range zeros: 0x{code_offset:X}:0x2000")
        f.seek(code_offset)
        f.write(b'\x00' * (file_size - code_offset))

        # writing code to new offset
        if 0x2000 - code_offset >= 0:
            print(f"Jupm offset code: 0x{code_offset:X} to 0x2000")
            f.seek(0x2000)
            f.write(jumpr)
        else:
            print("Initial code indentation causes 0x2000. Script cannot work correctly")
            input("Press Enter to close: error 4")
            exit(4)
            
        # change code offset
        print(f"0x20d: {int(code_offset/256):02x} -> 20")
        f.seek(0x20D)
        f.write(b"\x20")
        print(f"0x21d: {code_offset1[0]:02x} -> 20")
        f.seek(0x21D)
        f.write(b"\x20")

        # I don't fully understand what this is,
        # but it is responsible for executing the external flag block.
        print(f"0x211: {code_offset2[0]:02x} -> 20")
        f.seek(0x211)      
        f.write(b"\x10")
        print(f"0x212: {code_offset3[0]:02x} -> 20")
        f.seek(0x212)
        f.write(b"\x10")
        print(f"0x221: {code_offset4[0]:02x} -> 20")
        f.seek(0x221)
        f.write(b"\x10")
        print(f"0x222: {code_offset5[0]:02x} -> 20")
        f.seek(0x222)
        f.write(b"\x10")
        
        # Write a flag block
        print("Write flag block to: 0x1000")
        f.seek((0x1000))
        f.write(flag)

        # Path flag to unlock fastboot
        print(f"Fastboot lock state: 0x{fastboot_lock_state:02x} -> 00")
        f.seek(0x104C)
        f.write(b"\x00")

    print("Create new preloader to: {}".format(Path("preloader_path/boot1.bin").resolve()))

def read_flag_block(file_size: int):
    pattern_flag = bytes.fromhex("41 4E 44 5F 52 4F 4D 49 4E 46 4F 5F 76")
    with open(Path("preloader_path/boot1.bin"), "rb") as f: 
        data = f.read()
        if data.find(pattern_flag) != -1:
            print("Flag block find state: successfully")
            f.seek(data.find(pattern_flag))
            flag = f.read(0x77)
        else:
            print("Magic numbers of flag block not found! Use manual instruction or contact me.")
            choice  = input("Do you wish to continue without the flag block? (y/n) ")
            if choice.lower() == "y":
                flag = b""
            else:
                input("Press Enter to close: error 3")
                exit(3)
        f.seek(data.find(pattern_flag) + 0x4C)
        fastboot_lock_state = f.read(0x1)

        if hex(fastboot_lock_state[0]) == "0x22":
            print("lock state: 22 (lock)")
        else:
             print("lock state: unlock")

        return auto_path_preloader(flag, fastboot_lock_state[0], file_size)


def copy_preloader():
    makedirs("preloader_path", exist_ok=True)
    src = Path("boot1.bin")
    while True:
        try:
            if not src.exists():
                raise FileNotFoundError
            file_size = src.stat().st_size
            if file_size != normal_file_size:
                print(f"Expected file size - {0x400000} byte, received size - {file_size}.")
                choice = input("Ignore this and continue? (y/n) ")
                if choice.lower() == "y":
                    print(f"continue with file with size difference {normal_file_size - file_size} byte")
                else:
                    input("Press Enter to close: error 1")
                    exit(1)


            print("boot1.bin found state: successfully")
            with open(src, "rb") as f_org:
                dst = Path("preloader_path/boot1.bin")
                with open(dst, "wb") as f_pth:
                    f_pth.write(f_org.read())

            break

        except FileNotFoundError:
            print("boot1.bin found state: fail\nPlease use mtkclient to read your preloader (boot1).")
            choice = input("Repeat search? (y/n) ")
            if choice.lower() == "y":
                pass
            else:
                input("Press Enter to close: error 2")
                exit(2)

    return read_flag_block(file_size)

copy_preloader()
input("Press Enter to close ")
