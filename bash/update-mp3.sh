#!/usr/bin/env bash

echo mkdir -p "${1}"/mp3
mkdir -p "${1}"/mp3

echo cd "${1}"
cd "${1}"

echo 'cp -v */audio-out/*.mp3 mp3/'
cp -v */audio-out/*.mp3 mp3/

