class GoogleVerificationMiddleware:
    def __init__(self, app):
        self.app = app
        self.verification_tag = '<meta name="google-site-verification" content="UpK4x268-JAVGifEIIa0LG7x9OFnEFgoBqvRvdxio-E" />'

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            output_headers = []
            for header in headers:
                if header[0].lower() == 'content-type' and 'text/html' in header[1].lower():
                    # This is an HTML response, we'll need to modify it
                    return start_response(status, headers, exc_info)
                output_headers.append(header)
            return start_response(status, output_headers, exc_info)

        response = b''.join(self.app(environ, custom_start_response))
        
        # Only modify HTML responses
        if b'<!DOCTYPE html>' in response:
            # Insert verification tag after <head>
            head_pos = response.find(b'<head>')
            if head_pos != -1:
                modified_response = response[:head_pos + 6] + self.verification_tag.encode() + response[head_pos + 6:]
                return [modified_response]
        
        return [response]

# In your main.py, add this at the top:
import os
from middleware import GoogleVerificationMiddleware