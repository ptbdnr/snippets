access Azure JWT token and decode it

```shell
az login
JWT=$(az account get-access-token | jq -r .accessToken)
jq -R 'split(".") | .[1] | @base64d | fromjson' <<< "$JWT"
```
