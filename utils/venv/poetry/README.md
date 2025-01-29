Configure your Python development environment using Pyenv and Poetry

## Install OS package manager

MacOS: Homebrew

Simplify the installation of other utilities:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”
```

## Install Pyenv

Pyenv does not depend on Python.

with homebrew:
```bash
brew install pyenv
```

## Install Python

```bash
PYTHON_VERSION = 3.11
pyenv install $PYTHON_VERSION
```

Set a default global version of Python

```bash
pyenv global 3.11
```

(optional) Get the Latest Root Certificate Chain ans store it in `~/certs/chain.pem`

Change permission to allow owner to write, and all identities to read
```bash
chmod 644 ~/certs/chain.pem
```

Prove that the root certificate chain is valid:
```bash
openssl s_client -CAfile ~certs/chain.pem -connect pypi.org:443
```

expected output:
```
---
SSL handshake has read 2738 bytes and written 745 bytes
Verification: OK
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
This TLS version forbids renegotiation.
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 0 (ok)
---
```

Print Python environment default root certificate chain location (attribute name = 'cafile')

```bash
python -c "import ssl; print(ssl.get_default_verify_paths())"
```

expected output:
```
DefaultVerifyPaths(cafile='/usr/local/etc/openssl@1.1/cert.pem', capath=None, openssl_cafile_env='SSL_CERT_FILE', openssl_cafile='/usr/local/etc/openssl@1.1/cert.pem', openssl_capath_env='SSL_CERT_DIR', openssl_capath='/usr/local/etc/openssl@1.1/certs')
```

Set the Python environment variable SSL certificate authority file. And verify that attribute `cafile` is updated.

```bash
export SSL_CERT_FILE=~/certs/chain.pem
python -c "import ssl; print(ssl.get_default_verify_paths())"
```

## Install Python Poetry

Poetry creates Python virtual environments.
Poetry must be installed in an isolated location - separate to any Python project environment - using venv in this location `~/Library/Application Support/pypoetry`

```bash
curl -sSL https://install.python-poetry.org | python3 - --git https://github.com/python-poetry/poetry.git@main
```

add path to Poetry

```bash
export PATH="~/.local/bin:$PATH"
```

verify that Poetry is installed
```bash
poetry --version
~/Library/Application\ Support/pypoetry/venv/bin/python --version
```

`~/Library/Application\ Support/pypoetry/venv` is the Python virtual environment that Python Poetry uses to process requests.

To prevent any conflict between Python versions, configure Python Poetry:

```bash
poetry config virtualenvs.prefer-active-python true --local
```

## Create a New Project

New project

```bash
PROJECT_NAME = foo
poetry new "$PROJECT_NAME"
cd "$PROJECT_NAME"
cat pyproject.toml | grep “python = ”
```

New virtual environment

```bash
poetry self add poetry-plugin-shell
poetry shell
poetry env info
poetry -vvv add blackhole
```

(optional) identify the Python Poetry virtualenv `certifi` certificate directory, append the your root certificate chain to the `certifi` chain, and disable alternative certificate path locations

```bash
~/Library/Application\ Support/pypoetry/venv/bin/python -c "import certifi; print(certifi.where())"

cat ~/certs/chain.pem >> ~/Library/Application\ Support/pypoetry/venv/lib/python$PYTHON_VERSION/site-packages/certifi/cacert.pem

unset REQUESTS_CA_BUNDLE
```

verify
```bash
~/Library/Application\ Support/pypoetry/venv/bin/python -c "
import socket; import ssl
hostname = 'www.python.org'; context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())"
```