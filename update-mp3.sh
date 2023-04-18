#!env bash
echo cd "${1}"
cd "${1}"

echo 'cp -v */audio-out/*.mp3 mp3/'
cp -v */audio-out/*.mp3 mp3/

