from __future__ import annotations

import os
import sys
from pathlib import Path

from pygls import uris, workspace


class GlobalSettings(dict):
    def initialize(self, settings: dict) -> None:
        self.update(**settings)
        self.setdefault("interpreter", [sys.executable])


class WorkspaceSettings(dict):
    def initialize(self, settings: list[dict]) -> None:
        if not settings:
            key = os.getcwd()
            self[key] = {
                "cwd": key,
                "workspaceFS": key,
                "workspace": uris.from_fs_path(key),
                **GLOBAL_SETTINGS,
            }
            return
        for setting in settings:
            key = uris.to_fs_path(setting["workspace"])
            self[key] = {
                **setting,
                "workspaceFS": key,
            }

    def by_document(self, document: workspace.Document | None) -> dict:
        """
        Returns the workspace information for the given document.

        Args:
            document (workspace.Document | None): The document for which to retrieve workspace information.

        Returns:
            dict: A dictionary containing workspace information such as current working directory, workspace file system path,
            workspace URI, and global settings.
        """
        if document is None or document.path is None:
            return list(self.values())[0]
        key = self._get_document_key(document)
        if key is None:
            # This is either a non-workspace file or there is no workspace.
            key = os.fspath(Path(document.path).parent)
            return {
                "cwd": key,
                "workspaceFS": key,
                "workspace": uris.from_fs_path(key),
                **GLOBAL_SETTINGS,
            }
        return self[str(key)]

    def _get_document_key(self, document: workspace.Document) -> str | None:
        """
        Return the key of the document's workspace.

        Args:
            document (workspace.Document): The document to get the workspace key for.

        Returns:
            str | None: The key of the document's workspace if found, otherwise None.
        """
        document_workspace = Path(document.path)
        workspaces = {s["workspaceFS"] for s in self.values()}
        # Find workspace settings for the given file.
        while document_workspace != document_workspace.parent:
            if str(document_workspace) in workspaces:
                return str(document_workspace)
            document_workspace = document_workspace.parent
        return None

    def by_path(self, file_path: Path) -> dict:
        """
        Return the workspace corresponding to the given file path.

        Args:
            file_path (Path): The file path for which to find the corresponding workspace.

        Returns:
            dict: The workspace corresponding to the file path. If no matching workspace is found, returns the first workspace in the list of values.
        """
        workspaces = {s["workspaceFS"] for s in self.values()}
        while file_path != file_path.parent:
            str_file_path = str(file_path)
            if str_file_path in workspaces:
                return self[str_file_path]
            file_path = file_path.parent
        return list(self.values())[0]


SERVER_NAME = "chatgpt-docstrings"
SERVER_VER = "0.1"
MAX_WORKERS = 5
GLOBAL_SETTINGS = GlobalSettings()
WORKSPACE_SETTINGS = WorkspaceSettings()
