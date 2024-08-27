import sys
import ctypes

class Request:
    def __init__(self):
        # Interfaz to the Zig functions
        self.lib = ctypes.CDLL("./librequest_wrappers.so")
        self.lib.request_wrapper.argtypes = [ctypes.c_char_p]
        self.lib.request_wrapper.restype = ctypes.POINTER(ctypes.c_char)
    def get(self, url: str) -> str:
        # Executing the Zig request function
        result = self.lib.request_wrapper(url.encode())
        if not result:
            print("Fail request")
            sys.exit(1)
        # Finding the length of the array
        i = 0
        while result[i] != b'\0':
            i += 1
        content = result[:i].decode()
        self.lib.request_deallocate(result)
        return content

if __name__ == "__main__":
    # Check if the number of arguments is correct
    if len(sys.argv) < 2:
        print("Usage: %s URL" % sys.argv[0])
        sys.exit(1)
    # Obtaining the URL
    url = sys.argv[1]
    # Making a request
    req = Request()
    print(req.get(url))
