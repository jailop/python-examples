const std = @import("std");

// Adapted from:
// https://cookbook.ziglang.cc/05-01-http-get.html
pub fn request(allocator: std.mem.Allocator, url: []const u8) ![]u8 {
    const max_block = 1024 * 1024 * 4;
    var client = std.http.Client{ .allocator = allocator };
    defer client.deinit();
    const uri = try std.Uri.parse(url);
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

test "Retrieve" {
    const allocator = std.testing.allocator;
    const url = "http://localhost";
    const response = try request(allocator, url);
    defer allocator.free(response);
}
