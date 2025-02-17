#!/bin/bash

# Execute with `bash production.sh`	or `chmod +x production.sh` and then `./production.sh`

###### Step 1 - Optimization
# removes unnecessary dev dependencies.
composer install --optimize-autoloader --no-dev

# Clear caches
php artisan cache:clear && php artisan config:clear && php artisan route:clear
php artisan view:cache

# Build Front-end
npm run build


###### Step 2 - Zip Folder for Upload

# Ensure zip is installed
sudo apt install zip

#!/bin/bash

# Define project name dynamically (current directory name)
PROJECT_NAME=$(basename "$PWD")

# Define the builds directory
BUILD_DIR="ProdBuilds"

# Ensure the ProdBuilds directory exists
mkdir -p "$BUILD_DIR"

# Find the latest version number from existing zip files
LATEST_VERSION=$(ls "$BUILD_DIR" | grep -oP "Prod-${PROJECT_NAME}-V\K\d+" | sort -nr | head -n 1)

# If no version exists, start from 1, otherwise increment
if [[ -z "$LATEST_VERSION" ]]; then
    VERSION=1
else
    VERSION=$((LATEST_VERSION + 1))
fi

# Define the zip file name with the new version
ZIP_FILE="${BUILD_DIR}/Prod-${PROJECT_NAME}-V${VERSION}.zip"

# Remove any existing zip file with the same version (optional safety check)
rm -f "$ZIP_FILE"

# Create the zip archive excluding unnecessary files
zip -r "$ZIP_FILE" . -x "node_modules/*" ".git/*" "storage/logs/* ProdBuilds/*"

# Print success message
echo "Project successfully zipped as: $ZIP_FILE"

