all: request_test

librequest_wrappers.so: request_wrappers.zig request.zig
	zig build-lib -dynamic request_wrappers.zig

request_test: request_test.c librequest_wrappers.so
	zig cc -o request_test request_test.c -lrequest_wrappers -L.

clean:
	rm -f librequest_wrappers.so
	rm -f *.o
	rm -f request_test
