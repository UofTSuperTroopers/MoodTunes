#!/bin/bash
echo 'Organizing project folders...'
mkdir -p data/deam
mkdir -p data/librosa_features
mkdir -p audio_samples
mkdir -p scripts
mkdir -p notebooks

echo 'Creating .gitignore...'
cat <<EOL > .gitignore
*.mp3
*.wav
*.h5
__pycache__/
*.pyc
.DS_Store
.env
EOL
