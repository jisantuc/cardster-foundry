#!/bin/bash

set -e

profile=$1

cp ../ioutils.py ../requirements.txt .
pip install -t . -r requirements.txt

zip -r9 deploy_package.zip ./

aws --profile $profile lambda update-function-code \
    --function-name cardster_foundry_AllIssues \
    --zip-file fileb://deploy_package.zip

rm -r requests*/
rm deploy_package.zip ioutils.py requirements.txt
