import tiktoken

enc_cl100k_base = tiktoken.get_encoding("cl100k_base")
print(enc_cl100k_base.encode('Some text to encode'))