# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Contains the bookmarsks utilities.
"""
# Standard imports
import os.path as osp

# Local imports
from spyder.config.manager import CONF


def _load_all_bookmarks():
    """Load all bookmarks from config."""
    slots = CONF.get('editor', 'bookmarks', {})
    for slot_num in list(slots.keys()):
        if not osp.isfile(slots[slot_num][0]):
            slots.pop(slot_num)
    return slots


def load_bookmarks(filename):
    """Load all bookmarks for a specific file from config."""
    bookmarks = _load_all_bookmarks()
    return {k: v for k, v in bookmarks.items() if v[0] == filename}


def load_bookmarks_without_file(filename):
    """Load all bookmarks but those from a specific file."""
    bookmarks = _load_all_bookmarks()
    return {k: v for k, v in bookmarks.items() if v[0] != filename}


def save_bookmarks(filename, bookmarks):
    """Save all bookmarks from specific file to config."""
    if not osp.isfile(filename):
        return
    slots = load_bookmarks_without_file(filename)
    for slot_num, content in bookmarks.items():
        slots[slot_num] = [filename, content]
    CONF.set('editor', 'bookmarks', slots)


def get_free_bookmark_slot():
    """Get the lowest available bookmark slot."""
    # Limited to 99 bookmarks with current implementation
    bookmarks = _load_all_bookmarks()
    return min(set(range(1, 100)) - set(bookmarks.keys()))


def load_filenames_with_bookmarks():
    """Get all filenames that has at least one bookmark."""
    bookmarks = _load_all_bookmarks()
    return [v[0] for k, v in bookmarks.items()]
