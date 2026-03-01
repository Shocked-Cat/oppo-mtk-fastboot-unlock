from pathlib import Path
from os import makedirs
from sys import exit
import argparse

normal_file_size = 4 * 1024 * 1024

print("Dev. Max_Goblin - 4pda")

def auto_path_preloader(flag: bytes, fastboot_lock_state: bytes, file_size: int):
    with open(ndc, "r+b") as f:
        data = f.read()
        
        # read code offset
        code_offset = data[0x20d] * 256
        code_offset1 = data[0x21d]
        code_offset2 = data[0x211]
        code_offset3 = data[0x212]
        code_offset4 = data[0x221]
        code_offset5 = data[0x222]

        # read raw code
        data_raw = data[code_offset : file_size - 0x3000]

        # writing zeros
        print(f"Write range zeros: 0x{code_offset:X}:0x2000")
        f.seek(code_offset)
        f.write(b'\x00' * (file_size - code_offset))

        # writing raw code to new offset
        if 0x2000 - code_offset >= 0:
            print(f"Jump offset code: 0x{code_offset:X} to 0x2000")
            f.seek(0x2000)
            f.write(data_raw)
        else:
            print("Initial code indentation causes 0x2000. Script cannot work correctly")
            input("Press Enter to close: error 6")
            exit(6)
            
        # change code offset
        print("--------------------\nChange BRLYT offset")
        print(f"0x20d: {int(code_offset/256):02x} -> 20")
        f.seek(0x20D)
        f.write(b"\x20")
        print(f"0x21d: {code_offset1:02x} -> 20")
        f.seek(0x21D)
        f.write(b"\x20")
        print(f"0x211: {code_offset2:02x} -> 10")
        f.seek(0x211)      
        f.write(b"\x10")
        print(f"0x212: {code_offset3:02x} -> 10")
        f.seek(0x212)
        f.write(b"\x10")
        print(f"0x221: {code_offset4:02x} -> 10")
        f.seek(0x221)
        f.write(b"\x10")
        print(f"0x222: {code_offset5:02x} -> 10")
        f.seek(0x222)
        f.write(b"\x10")
        
        # Write a flag block
        print("--------------------\nWrite flag block to: 0x1000")
        f.seek((0x1000))
        f.write(flag)

        # Change flag to unlock fastboot
        print(f"Fastboot lock state: 0x{fastboot_lock_state[0]:02x} -> 00")
        f.seek(0x104C)
        f.write(b"\x00")

    print("Create new preloader to: {}".format(ndc.resolve()))

def read_flag_block(file_size: int):
    pattern_flag = bytes.fromhex("41 4E 44 5F 52 4F 4D 49 4E 46 4F 5F 76")
    with open(ndc, "rb") as f: 
        data = f.read()
        patt_stat = data.find(pattern_flag)
        if patt_stat != -1:
            print("Flag block find state: successfully")
            flag = data[patt_stat : patt_stat + 0x78]
            patt_lock = patt_stat + 0x4C
            fastboot_lock_state = data[patt_lock : (patt_lock + 1)]
        else:
            print("Magic numbers of flag block not found! Use manual instruction or contact me.")
            choice  = input("Do you wish to continue without the flag block? (y/n) ")
            if choice.lower() == "y":
                flag = b""
                fastboot_lock_state = 0x0
            else:
                input("Press Enter to close: error 5")
                exit(5)

        if hex(fastboot_lock_state[0]) == "0x22":
            print("lock state: 22 (lock)")
        elif hex(fastboot_lock_state[0]) == "0x11":
            print("lock state: 11 (hard lock)")
        else:
            print(f"lock state: {fastboot_lock_state[0]} (unlock)")

        return auto_path_preloader(flag, fastboot_lock_state, file_size)


def check_validation():
        file_size = ndc.stat().st_size
        if file_size != normal_file_size:
            print(f"Expected file size - 0x400000 byte, received size - {hex(file_size)}.")
            choice = input("Ignore this and continue? (y/n) ")
            if choice.lower() == "y":
                print(f"continue with file with size difference {hex(normal_file_size - file_size)} byte")
            else:
                input("Press Enter to close: error 2")
                exit(2)

        with open(ndc, "rb") as f:
            magic_sign = f.read(0x10)
            
        if magic_sign.startswith(b"UFS_BOOT"):
            print("Memory type: UFS_BOOT")
        elif magic_sign.startswith(b"EMMC_BOOT"):
            print("Memory type: EMMC_BOOT")
        elif magic_sign.startswith(b"COMBO_BOOT"):
            print("Memory type: COMBO_BOOT (UFS)")
        elif magic_sign.startswith(b"MMM\x018\x00\x00\x00FILE_INF"):
            print("Memory type: RAW\n\nThis script cannot work with RAW preloader.\nRAW preloader is not a full-fledged boot1 region and does not have an offset header, which this script works with.")
            input("Press Enter to close: error 3")
            exit(3)
        else:
            print(f"Memory type: {magic_sign} (Unknown)")
            choice = input("\nScript execution outcome may be unpredictable, continue? (y/n) ")
            if choice.lower() != "y":    
                input("Press Enter to close: error 4")
                exit(4)
        
        return read_flag_block(file_size)

def copy_preloader():
    makedirs("preloader_path", exist_ok=True)
    while True:
        try:
            with open(ndo, "rb") as f_ndo:
                with open(ndc, "wb") as f_ndc:
                    f_ndc.write(f_ndo.read())

            print(f"{ndo.name} found state: successfully")

            break

        except FileNotFoundError:
            print(f"{ndo.name} found state: fail\nPlease use mtkclient to read your preloader {ndo.name}.")
            choice = input("Repeat search? (y/n) ")
            if choice.lower() != "y":
                input("Press Enter to close: error 1")
                exit(1)

    return check_validation()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Script for modifying the factory preloader to provide access to fastboot."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="The path or name of the preloader input file. Defaults to boot1.bin."
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="The output file name (result in preloader_path/). By default, it matches the input file name."
    )
    args = parser.parse_args()
    return args.file, args.output


def main():
    global ndo, ndc
    source, output_name = parse_args()

    if source is None:
        ndo = Path("boot1.bin")
        ndc = Path("preloader_path/boot1.bin")
        print("Mode: Default")
    else:
        ndo = Path(source)
        out_file = output_name if output_name is not None else ndo.name
        ndc = Path("preloader_path") / out_file
        print("Mode: CLI")

    copy_preloader()
    input("Press Enter to close ")

if __name__ == "__main__":
    main()
