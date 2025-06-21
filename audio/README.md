# Audio Files Directory

This directory contains the audio narration files for the heritage sites in the Itihaas application.

## Required Audio Files

For the audio feature to work properly, you should add the following files:

1. **default_narration.mp3** - Default fallback narration used when no specific audio is available
2. **[category]_narration.mp3** - Category-specific narrations:
   - temple_narration.mp3
   - fort_narration.mp3
   - palace_narration.mp3
   - monument_narration.mp3
3. **narration_[siteId].mp3** - Site-specific custom narrations for important sites

## How to Create Audio Files

You can generate these audio files using:
1. Text-to-speech services like Google Cloud TTS, Amazon Polly, or Microsoft Azure Speech Service
2. Free online TTS tools
3. Recording professional voice-over narrations

## Audio Content

The scripts for each audio file are provided in the `create_audio.txt` file in this directory.

## Alternative Audio Playback

If audio files are not available, the application will fall back to using the browser's Speech Synthesis API as a last resort. However, for the best user experience, it's recommended to provide actual audio files.

## Testing

For quick testing without creating actual audio files, you can use online text-to-speech tools to generate a single default_narration.mp3 file. 