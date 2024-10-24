#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: This script is designed to delete files older than a specified age from a defined directory.

Environment Variables:
    ICA_FILES_DELETE_LOCK_FILE: The location of the lock file.
                                 Defaults to /tmp/ica_delete_service.lock
    ICA_MAX_LOCK_FILE_AGE: Maximum age of lock file in seconds.
                                 Defaults to 300 seconds (5 minutes).
    ICA_DELETE_SERVICE_ROOT_DIR: The root directory from which files will be deleted.
                                 Defaults to '/app/public' if not specified.
    ICA_DELETE_SERVICE_MAX_FILE_AGE: The maximum age (in seconds) that files are allowed to remain in the directory.
                                     Defaults to 86400 seconds (24 hours) if not specified.
"""

import logging
import os
import time

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Default values for environment variables if not defined
DEFAULT_ROOT_DIR: str = "/app/public"  # Default root directory
DEFAULT_MAX_FILE_AGE: int = 24 * 60 * 60  # Default max file age (1 day in seconds)
ICA_FILES_DELETE_LOCK_FILE: str = "/tmp/ica_delete_service.lock"
ICA_MAX_LOCK_FILE_AGE: int = 300  # 5 minutes


def acquire_lock() -> bool:
    """Tries to acquire a lock by creating a lock file.

    If the lock file exists and is older than ICA_MAX_LOCK_FILE_AGE, it will be deleted
    and the function will attempt to lock again.

    Returns:
        bool: True if the lock was successfully acquired, False otherwise.
    """
    try:
        if os.path.exists(ICA_FILES_DELETE_LOCK_FILE):
            file_age = time.time() - os.path.getmtime(ICA_FILES_DELETE_LOCK_FILE)
            if file_age > ICA_MAX_LOCK_FILE_AGE:
                os.remove(ICA_FILES_DELETE_LOCK_FILE)
                log.info("Removed stale lock file: age %s seconds", file_age)

        with os.fdopen(
            os.open(ICA_FILES_DELETE_LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY),
            "w",
        ) as f:
            f.write(f"Locked by PID {os.getpid()} at {time.time()}")
        log.info("Lock successfully acquired")
        return True
    except FileExistsError:
        log.error("Lock file already exists. Another instance is running.")
        return False


def release_lock():
    """Releases the acquired lock by deleting the lock file."""
    try:
        os.remove(ICA_FILES_DELETE_LOCK_FILE)
        log.info("Lock file removed.")
    except OSError as e:
        log.error("Failed to remove lock file: %s", e)


def delete_old_files(directory: str, max_file_age: int):
    """Recursively deletes files older than `max_file_age` seconds in the specified directory.

    Args:
        directory (str): The directory to delete files from.
        max_file_age (int): The maximum age of files to keep, in seconds.

    Examples:
        >>> import os
        >>> os.makedirs('/tmp/ica_test', exist_ok=True)
        >>> with open('/tmp/ica_test/old_file.txt', 'w') as f:
        ...     f.write('old file')
        >>> os.path.exists('/tmp/ica_test/old_file.txt')
        True
        >>> delete_old_files('/tmp/ica_test', 0)  # immediate deletion
        Deleted /tmp/ica_test/old_file.txt: age ...
        >>> os.path.exists('/tmp/ica_on_test/old_file.txt')
        False
    """
    current_time: float = time.time()

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_age = current_time - os.path.getmtime(file_path)
            log.debug(f"Found: {file_path} with file_age: {file_age}, comparing to max_file_age: {max_file_age}")
            if file_age > max_file_age:
                try:
                    os.remove(file_path)
                    log.info("Deleted %s: age %s seconds", file_path, file_age)
                except OSError as e:
                    log.error("Error deleting %s: %s", file_path, e)
                log.debug(
                    "Checking file %s with age %s against max age %s",
                    file_path,
                    file_age,
                    max_file_age,
                )


if __name__ == "__main__":
    root_dir = os.getenv("ICA_DELETE_SERVICE_ROOT_DIR", DEFAULT_ROOT_DIR)
    max_age = int(os.getenv("ICA_DELETE_SERVICE_MAX_FILE_AGE", str(DEFAULT_MAX_FILE_AGE)))

    if acquire_lock():
        try:
            log.debug(f"Calling delete_old_files({root_dir},{max_age})")
            delete_old_files(root_dir, max_age)
        finally:
            release_lock()
