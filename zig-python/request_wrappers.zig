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

export fn request_deallocate(result: [*:0]u8) void {
    const allocator = std.heap.page_allocator;
    // const allocator = std.testing.allocator;
    const len = std.mem.len(result) + 1;
    allocator.free(result[0..len]);
}

test "Wrappers" {
    const url = "http://localhost";
    const body = request_wrapper(url.ptr);
    try std.testing.expect(std.mem.len(body.?) > 0);
    request_deallocate(body.?);
}
