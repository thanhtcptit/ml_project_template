#!/bin/bash

bash -c 'rsync -avz $(pwd) $(cat .xenv/host) --exclude .git'