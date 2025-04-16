This is a [Next.js](https://nextjs.org) project, based on the [deployment documentation](https://nextjs.org/docs/deployment#docker-image).

# :wrench: Developer Guide

## Requirements

* node v18 or later: https://nodejs.org/en/download
* Docker: https://docs.docker.com/get-docker/
* Vultr account with:
    * Container Registry
    * Compute instance


## Clone the repo

Connect your host to GitHub
1. [Create a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
    * `ssh-keygen -t ed25519 -C "your_email@example.com"`
    * `eval "$(ssh-agent -s)"`
    * `ssh-add ~/.ssh/id_ed25519`
2. [Add a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
    * `cat ~/.ssh/id_ed25519.pub`
    * In GitHub, Settings / Access section, click  SSH and GPG keys. Click New SSH key or Add SSH key. In the "Title" field be creative. In the "Key" field, paste your public key.

```shell
git clone git@github.com:ptbdnr/snippets
```


## Copy the environment variables to the project root

source: ask!

```shell
cat << EOF > .env.local
KEY1=VALUE1
KEY2=VALUE2
EOF
```


### Evaluate dependencies

```shell
cd nextjs_js
(ls .env.local && echo 'INFO: Found .env.local') || echo 'CRITICAL: Missing .env.local'
(ls package.json && echo 'INFO: Found package.json') || echo 'CRITICAL: Missing package.json'
```


### 🏃 Running Locally

```shell
npm install
# or
pnpm install
```

```shell
npm run dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.


# Contribution

You can start editing the page by modifying `pages/index.js`. The page auto-updates as you edit the file.

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.js`.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.


### Deploy to VM with Docker

Ensure the following is in the `next.config.js` file:

```js
// next.config.js
module.exports = {
  // ... rest of the configuration.
  output: "standalone",
};
```

Ensure Docker daemon is running on your machine.

```shell
# Build the image, 
# optionally add `--no-cache` to force a fresh build
docker build --progress=plain -t ptbdnr/$IMAGE_NAME:$TAG .

# List all running containers
docker ps

# Stop container running on port 3000
docker stop $(docker ps -q --filter "name=$CONTAINER_NAME")

# Quick test
docker run -p 3000:3000 ptbdnr/$IMAGE_NAME:$TAG
```

```shell
# [OPTIONAL] Pull yout latest image if not already on the machine
docker pull ptbdnr/$IMAGE_NAME:latest
# on macOS you might need the suffix `--platform linux/x86_64`

# List all images available locally
docker imagess

# Log into Vultr Container Registry 
docker login https://ams.vultrcr.com/container_registry -u $CR_USER -p $CR_PASS

# Tag and Push your image to Vults Container Registry
docker tag ptbdnr/$IMAGE_NAME:latest ams.vultrcr.com/container_registry/$IMAGE_NAME:latest
docker push ams.vultrcr.com/container_registry/$IMAGE_NAME:latest
```

On the server, ensure Docker is installed

```shell
apt  install docker.io

# Below is Optional but recommended
# Create user `docker`
useradd -m -g users docker
# create user group `dockergroup`
sudo addgroup dockergroup
# add users to user group
usermod --append --groups dockergroup docker
usermod --append --groups dockergroup $ADMIN_USER
# switch to the `docker` user
su - docker
```

```shell
# Log into Vultr Container Registry 
docker login https://ams.vultrcr.com/container_registry -u $CR_USER -p $CR_PASS

# Pull yout latest image
docker pull ams.vultrcr.com/container_registry/$IMAGE_NAME:latest
# on macOS you might need the suffix `--platform linux/x86_64`

# List all images available locally
docker images

# List all running containers
docker ps

# Stop container running on port 3000
docker stop $(docker ps -q --filter "name=$CONTAINER_NAME")

# Run image in detached mode, optionally add `--name $CONTAINER_NAME`
docker run -d -p 3000:3000 ams.vultrcr.com/container_registry/$IMAGE_NAME
```
