# Compression and Archiving Command Examples

## tar
`tar` is used to create and extract archive files.

```bash
# Create a tar archive named archive.tar containing the contents of a directory
tar -cvf archive.tar /path/to/directory

# Extract a tar archive
tar -xvf archive.tar

# Create a compressed tar.gz archive
tar -czvf archive.tar.gz /path/to/directory

# Extract a tar.gz archive
tar -xzvf archive.tar.gz
```

## gzip
`gzip` compresses files using the Lempel-Ziv coding (LZ77) algorithm.

```bash
# Compress a file with gzip
gzip filename

# This replaces the original file with a compressed file (filename.gz)
```

## gunzip
`gunzip` decompresses files compressed by gzip.

```bash
# Decompress a gzipped file and restore the original file
gunzip filename.gz
```

## zip
`zip` is used to create compressed archive files in ZIP format.

```bash
# Create a zip archive containing a file
zip archive.zip filename

# Create a zip archive including all files in a directory
zip -r archive.zip /path/to/directory
```

## unzip
`unzip` is used to extract files from a zip archive.

```bash
# Extract all files from a zip archive
unzip archive.zip

# Extract files to a specific directory
unzip archive.zip -d /path/to/destination
```