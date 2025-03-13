# Package Management Command Examples

## apt-get
`apt-get` is used on Debian-based systems, including Ubuntu.

```bash
# Update package lists
sudo apt-get update

# Install a package
sudo apt-get install package-name

# Remove a package
sudo apt-get remove package-name

# Upgrade installed packages
sudo apt-get upgrade
```

## brew
`brew` (Homebrew) is a popular package manager for macOS (and Linux).

```bash
# Update Homebrew and formulae
brew update

# Install a package
brew install package-name

# Remove a package
brew uninstall package-name

# Upgrade installed packages
brew upgrade
```

## yum
`yum` is commonly used in older Fedora, CentOS, and RHEL systems.

```bash
# Install a package
sudo yum install package-name

# Remove a package
sudo yum remove package-name

# Update all packages
sudo yum update
```


## dnf
`dnf` is the default package manager for Fedora and related distributions.

```bash
# Install a package
sudo dnf install package-name

# Remove a package
sudo dnf remove package-name

# Update all packages
sudo dnf update
```
