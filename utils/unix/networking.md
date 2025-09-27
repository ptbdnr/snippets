# Networking Command Examples

## ping
`ping` checks the network connectivity between your machine and a remote host.
  
```bash
# Send ICMP echo requests continuously (press Ctrl+C to stop)
ping example.com

# Send a fixed number of 4 echo requests and then stop
ping -c 4 example.com
```

## wget
`wget` is a network downloader, useful for downloading files from the web.
  
```bash
# Download a file from a URL
wget http://example.com/file.zip

# Download a file and save it with a different name
wget -O newname.zip http://example.com/file.zip
```

## cURL
`curl` is a tool for transferring data with URL syntax, supporting various protocols.
  
```bash
# Retrieve the contents of a web page and display on the terminal
curl http://example.com

# Download a file and save it locally
curl -o file.zip http://example.com/file.zip

# Follow redirects while retrieving a file
curl -L -o file.zip http://example.com/file.zip

# query and API
curl https://api.perplexity.ai/search \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": [
      "What is Comet Browser?",
      "Perplexity AI",
      "Perplexity Changelog"
    ]
  }' | jq
```

## ssh
`ssh` is used to securely connect to remote systems over a network.
  
```bash
# Connect to a remote server using the default SSH port
ssh user@example.com

# Connect to a remote server specifying a custom port
ssh -p 2222 user@example.com
```

## scp
`scp` is used to securely copy files between hosts on a network.

```bash
# Copy a local file to a remote server
scp localfile.txt user@example.com:/remote/path/

# Copy a remote file to the local machine
scp user@example.com:/remote/path/remote.txt ./localfolder/

# Recursively copy an entire directory
scp -r localdir user@example.com:/remote/path/
```

## ftp
`ftp` is used for file transfer between a local and a remote host using the FTP protocol.  
  
```bash
# Connect to an FTP server
ftp ftp.example.com

# Once connected, typical commands include:
# - user: to log in (e.g., user yourusername)
# - get: to download a file (e.g., get filename)
# - put: to upload a file (e.g., put localfile)
# type 'help' or 'mhelp' for a list of available commands
```