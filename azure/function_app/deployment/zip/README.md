# ZIP deployment

## Quick deploy
```shell
func azure functionapp publish $FUNCTION_APP_NAME
```

## Manual zip then upload

Create a zip file of the code, then deploy it (via storage account)

Input arguments:
    * PATH_TO_ROOT_DIR is the path to the project root directory that contains host.json and function_app.py, currently this assumes that all relevant files are in the root directory, for example C:\workspace\fa-test
    * ZIP_FILENAME is the name of the zip file
    * LIST_OF_EXCLUDED_DIRS is the list of excluded directories

Replace placeholders with actual values (e.g., ZIP_FILENAME='my-deployment').

Azure Functions deployment via zip excludes unnecessary files for faster uploads.

on Windows

```powershell
# Note: Update {LIST_OF_EXCLUDED_DIRS} manually or create a script to read .funcignore."
$files = Get-ChildItem -Path "{PATH_TO_ROOT_DIR}\*" -Exclude {LIST_OF_EXCLUDED_DIRS}
Compress-Archive -Path $files -DestinationPath "{ZIP_FILENAME}.zip" -CompressionLevel "Optimal"
```

on macOS

```shell
# Create a zip archive while excluding files and directories listed in `.funcignore`.
# This snippet is compatible with bash/zsh. It ignores blank lines and lines starting with '#'.
# It adds both the literal entry and a wildcard for its children so directories are excluded too.
ZIP_FILENAME="{ZIP_FILENAME}"
excludes=()
while IFS= read -r line || [[ -n "$line" ]]; do
  # strip leading/trailing whitespace
  line="$(echo "$line" | awk '{$1=$1;print}')"
  # skip empty lines and comments
  [[ -z "$line" || ${line:0:1} == '#' ]] && continue
  # add pattern and pattern/* to exclude directories and their contents
  excludes+=("$line" "$line/*")
done < .funcignore

# create the zip using expanded exclude patterns
zip -r "${ZIP_FILENAME}.zip" . "${excludes[@]}"
rm $ZIP_FILENAME.zip
```

```shell
# sign in to azure account
az login
# deploy the zip file to Azure Function App
az functionapp deployment source config-zip --resource-group {RESOURCE_GROUP} --name {FUNCTION_APP_NAME} --src "{ZIP_FILENAME}.zip"
```

## Troubleshooting

1. Open https://portal.azure.com/#home in your browser
2. Go to your Function App
3. On the left navigation panel, select "Diagnose and solve problems"
4. Search for "Functions that are not triggering"
5. Wait 10-20s
