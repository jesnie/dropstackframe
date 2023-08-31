#!/bin/env bash

set -e

git fetch origin main
git checkout main
git pull --rebase origin main
if ! git checkout -b dropstackframe; then
    git branch -D dropstackframe
    git checkout -b dropstackframe
fi
poetry run python -m requirements
if [[ $(git status --porcelain) ]]; then
    poetry update
    git \
        -c "user.name=Update requirements bot" \
        -c "user.email=none" \
        commit \
        -am "Update requirements."
    git push origin +dropstackframe
    gh pr create \
       --title "Update requirements" \
       --body "Automatic update of requirements."
       --reviewer jesnie
    false
fi
