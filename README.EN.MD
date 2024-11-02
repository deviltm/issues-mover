Here’s an improved and grammatically-corrected version of the README in English:

---

# Task Migration from YouTrack to Gitea with Attachment Support

This script transfers tasks from YouTrack to Gitea, with options to include labels, statuses, and upload attachments.

## Requirements

- **Python 3.7+**
- `requests` and `python-dotenv` modules (install with `pip install requests python-dotenv`)

## Configuration

1. **Create a `.env` file** in the root directory of the project and add the following parameters:

    ```env
    YOUTRACK_URL=https://youtrack.example.com
    YOUTRACK_TOKEN=your_youtrack_token
    GITEA_URL=https://gitea.example.com
    GITEA_TOKEN=your_gitea_token
    GITEA_OWNER=repository_owner
    GITEA_REPO=repository_name
    YOUTRACK_PROJECT=youtrack_project_name
    DOWNLOAD_FOLDER=./downloads
    ENABLE_ATTACHMENTS=true
    ENABLE_COMMENTS=true
    ```

2. **Running the script**:

    You can run the script from the command line, specifying the required parameters. Command-line parameters override those in the `.env` file.

    ```bash
    python main.py --youtrack_url <URL> --youtrack_token <TOKEN> --gitea_url <URL> --gitea_token <TOKEN> --gitea_owner <OWNER> --gitea_repo <REPO> --youtrack_project <PROJECT> --enable_attachments --enable_comments
    ```

    **Parameters:**

    - `--youtrack_url`: URL to access YouTrack
    - `--youtrack_token`: API token for YouTrack
    - `--gitea_url`: URL to access Gitea
    - `--gitea_token`: API token for Gitea
    - `--gitea_owner`: Repository owner name
    - `--gitea_repo`: Repository name
    - `--youtrack_project`: YouTrack project name
    - `--download_folder`: Path to save attachments (default is `./downloads`)
    - `--enable_attachments`: Flag to enable attachment uploads to Gitea (disabled by default)

## Features

- Transfers task labels and statuses from YouTrack to Gitea.
- Uploads attachments if the `--enable_attachments` flag is activated.
- Uploads task comments with attachments if the `--enable_comments` flag is activated.
- Task statuses from YouTrack are mapped to automatically close tasks in Gitea when created. Currently, these statuses are manually set in `gitea.py` on lines 99 and 107 as `close_label` and `open_label`. These labels in YouTrack determine the status and select the appropriate Gitea label for the task. Ensure that these labels are predefined in Gitea. See an example of labels in `labels.yaml`.
- New tasks automatically assign users as per YouTrack's assignees. Note that the presence of the same assignee in Gitea is not verified, which may cause issues during task addition.
- Tasks are skipped on errors.
- A log file (`log.txt`) is automatically maintained for `info` and `error` entries.
- Tested with 2000 and 1500 tasks.
- Disable all hooks and notifications during migration to avoid spam.
- Tasks are created under the user whose token is used, requiring full permissions.
- It is currently impossible to set the creator and creation time of tasks through the API; for this, task creation would need to be rewritten directly into the database.

## License

This project is available under the MIT License. See the `LICENSE` file for details.
