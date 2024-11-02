# Transfer Issues from YouTrack to Gitea with Attachments Support

This script transfers issues from YouTrack to Gitea, along with labels, statuses, and attachments.

## Requirements

- **Python 3.7+**
- Modules `requests` and `python-dotenv` (install via `pip install requests python-dotenv`)

## Setup

1. **Create a `.env` file** in the project root with the following parameters:

   ```env
   YOUTRACK_URL=https://youtrack.example.com
   YOUTRACK_TOKEN=your_youtrack_token
   GITEA_URL=https://gitea.example.com
   GITEA_TOKEN=your_gitea_token
   GITEA_OWNER=repo_owner
   GITEA_REPO=repo_name
   YOUTRACK_PROJECT=youtrack_project_name
   DOWNLOAD_FOLDER=./downloads
   ENABLE_ATTACHMENTS=true
   ```

2. **Running the Script**:

   The script can be run from the command line, specifying required parameters. Command-line arguments take precedence over `.env` variables.

   ```bash
   python main.py --youtrack_url <URL> --youtrack_token <TOKEN> --gitea_url <URL> --gitea_token <TOKEN> --gitea_owner <OWNER> --gitea_repo <REPO> --youtrack_project <PROJECT> --enable_attachments
   ```

   **Parameters:**

   - `--youtrack_url`: YouTrack URL
   - `--youtrack_token`: API token for YouTrack
   - `--gitea_url`: Gitea URL
   - `--gitea_token`: API token for Gitea
   - `--gitea_owner`: Repository owner name
   - `--gitea_repo`: Repository name
   - `--youtrack_project`: YouTrack project name
   - `--download_folder`: Path to save attachments (default: `./downloads`)
   - `--enable_attachments`: Flag to enable attachment uploads to Gitea (default: disabled)

## Features

- Transfers issue labels and statuses from YouTrack to Gitea.
- Uploads attachments if `--enable_attachments` is specified.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
