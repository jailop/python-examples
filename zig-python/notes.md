[DRAFT, WORK IN PROGRESS, DON'T CITE]

# Calling Zig functions from Python

Python, besides being a friendly programming languages, makes it easy to call C functions. Given that Zig shared the same ABI with C, it is the same as easy to call Zig functions from Python. This feature makes you able to write programs that shows a Python's friendly interface supported by extended and performant Zig's functions. In this article, a non-trivial example is shown: a program to make HTTP requests.

## Zig request function

As first step, we define the function prototype for the request function:

```zig
pub fn request(allocator: std.mem.Allocator, url: []const u8) ![]u8
```

Our `request` function will receive two arguments:

* `allocator`: An memory allocator object
* `url`: Request address represented as an sequence of bytes

This function will return an optional with two possible values: the content for the requested resource, or an error value. If the requested content is returned, memory allocated for it should be freed.

Adapted from the [Zig Cookbook](https://cookbook.ziglang.cc/05-01-http-get.html), here is an implementation for the `request` function:

```zig
const std = @import("std");

pub fn request(allocator: std.mem.Allocator, url: []const u8) ![]u8 {
    const uri = try std.Uri.parse(url);
    var client = std.http.Client{ .allocator = allocator };
    defer client.deinit();
    const max_block = 1024 * 1024 * 4;
    const buf = try allocator.alloc(u8, max_block);
    defer allocator.free(buf);
    var req = try client.open(.GET, uri, .{.server_header_buffer = buf});
    defer req.deinit();
    try req.send();
    try req.finish();
    try req.wait();
    var reader = req.reader();
    const body = try reader.readAllAlloc(allocator, max_block);
    return body;
}
```

Operations performed by this function are listed below. In case, any of these operations fails, an error is returned. Clean up operations are instructed using the keywork `defer`.

* `url` validation
* http client initialization
* buffer allocation to read data from the server
* openning the conection
* retrieving data
* returnning content

To check if this function works properly, here a test:

```zig
test "Request" {
    const allocator = std.testing.allocator;
    const url = "http://localhost";
    const response = try request(allocator, url);
    defer allocator.free(response);
}
```

If the `request` function and its test are saved in a file named `request.zig`, you can run this command to run the test:

```bash
$ zig test reques.zig
All 1 tests passed.
```

## Like-C function wrappers

In order to use the `request` function as C code, a few adjustments are needed:

* Strings are represented as `\0` terminated arrays
* Strings are passed using C pointers
* A explicit function to deallocated used memory will be provided

Prototypes for the request wrapper and the request deallocator functions are presented below:

```
export fn request_wrapper(url: [*:0]const u8) ?[*:0]u8
export fn request_deallocate(result: [*:0]u8) void
```

Notice that arguments are array pointers with 0 sentinel value. The return type for `request_wrapper` is an optional, i.e. its value can be `null`. Memory to store the HTTP response is allocated in `request_wrapper`and is released in `request_deallocate`.

Here is the implementation for `request_wrapper`:

```zig
const std = @import("std");
const request = @import("request.zig").request;

export fn request_wrapper(url: [*:0]const u8) ?[*:0]u8 {
    const len = std.mem.len(url);
    const url_sized = url[0..len];
    const allocator = std.heap.page_allocator;
    const resp = request(allocator, url_sized) catch return null;
    defer allocator.free(resp);
    const response = allocator.dupeZ(u8, resp) catch return null;
    return response;
}
```

In order to convert the `url` from `[*:0]const u8` to `[]const u8`, the lenght of `url` is computed and anew slice is created using the index notation: `url[0..len]`. In this wrapper function, the page allocator is used. It works similar to the `malloc`/`free` C functions. After the request is performed, data is transformed from `[]u8` to `[*:0]u8` using the function `allocator.dupez`. If any error occurs, a `null` value is returned.

Implementation for `request_deallocate` is shown bellow. It computes the length of the used memory, including the `\0` sentinal. Memory is deallocated using the `free` function of the page allocator.

```zig
export fn request_deallocate(result: [*:0]u8) void {
    const allocator = std.heap.page_allocator;
    // const allocator = std.testing.allocator;
    const len = std.mem.len(result) + 1;
    allocator.free(result[0..len]);
}
```

The keyword `export` is include to enabled this functions to be called from C and Python.

To test these functions, here is a test:

```zig
test "Wrappers" {
    const url = "http://localhost";
    const body = request_wrapper(url.ptr);
    try std.testing.expect(std.mem.len(body.?) > 0);
    request_deallocate(body.?);
}
```

Assuming the previous functions are saved in a file named `request_wrappers.zig`, you can run the tests using this command:

```bash
$ zig test request_wrappers.zig 
All 2 tests passed.
```

## Calling Zig from C

Before calling the previous Zig functions from Python, for testing they are called from C. For that, it is convenient to have a header file with the functions prototypes wrote in C style.

```C
#ifndef _RETRIEVER_H
#define _RETRIEVER_H 0

char *request_wrapper(const char *url);
void request_deallocate(char *content);

#endif // _RETRIEVER_H
```

Here is an example of a C program calling the `request` functions. This program expects the URL as its argument, otherwise an error is reported.

```C
#include <stdio.h>
#include <stdlib.h>
#include "request.h"

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s URL\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    const char *url = argv[1];
    char *content = request_wrapper(url);
    if (!content)
        printf("Failed\n");
    printf("%s\n", content);
    request_deallocate(content);
    return 0;
}
```

Assuming the previous program is saved in a file named `request_test.c`, to compile and run this C program, you can use these commands:

```bash
$ zig build-lib -dynamic request_wrappers.zig
$ zig cc -o request_test request_test.c -lrequest_wrappers -L.
$ ./request_test http://localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
...
```

Observe in the previous example that the first line is creating a dynamic library. If you're working on a Linux machine, the library filename will be `librequest_wrappers.so`.

## Calling Zig from Python

We're ready to call the `request` functions from Python.

In this example, the `ctypes` built-in library is used to build a `Request` class. In the `__init__` method, the matching to the `request_wrapper` funcion arguments and return type are defined. The `get` method is responsible to execute the request and deallocate the memory used.

```python
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
```

If the previous class is saved in a file named `request_zig.py`, it be called from Python as is shown in the next example:

```python
import request_zig
req = request_zig.Request()
req.get("http://localhost")
```
