# YouTube Video Editor Action

This repository contains a GitHub Action to download, clip, and concatenate segments from a YouTube video.

## How to use

1.  Go to the **Actions** tab in your GitHub repository.
2.  Select the **Edit YouTube Video** workflow.
3.  Click **Run workflow**.
4.  Enter the **YouTube Video URL**.
5.  Enter the **Timeline list** (e.g., `01:10-01:15, 03:20-03:35`).
6.  Select the **Download Method** (default is `auto`).
7.  Click **Run workflow**.
8.  Once finished, the edited video will be available as an artifact named `final_video`.

## Troubleshooting Bot Detection

If the workflow fails with an error like "Sign in to confirm you’re not a bot", you have a few options:

### 1. Change Download Method
Try switching the **Download Method** input. Some methods (like `yt-dlp-android`) use different player clients that might bypass detection. Using `auto` will try all methods sequentially.

### 2. Provide Cookies
1.  Use a browser extension like "Get cookies.txt LOCALLY" to export your YouTube cookies in Netscape format.
2.  In your GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
3.  Create a new repository secret named `COOKIES` and paste the contents of your cookies file.
4.  Run the workflow again.

## Timeline Format

The timeline should be a comma-separated list of time ranges. Each range should be in the format `START-END`, where `START` and `END` can be in `MM:SS` or `HH:MM:SS` format.

Example: `01:10-01:15, 03:20-03:35, 06:45-07:05, 10:15-10:25`
