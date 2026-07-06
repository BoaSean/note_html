#!/usr/bin/env python3
"""开发服务器，自动禁用浏览器缓存。用法：python3 server.py"""
import http.server

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

print('http://localhost:8000  (无缓存)')
http.server.HTTPServer(('', 8000), NoCacheHandler).serve_forever()
