"""
Media Type Constants
Author: fdygt
Created: 2025-06-04 16:25:57
"""

# Image Types
IMAGES = {
    'JPEG': {
        'extension': ['jpg', 'jpeg'],
        'mime': 'image/jpeg',
        'max_size': 10 * 1024 * 1024  # 10MB
    },
    'PNG': {
        'extension': ['png'],
        'mime': 'image/png',
        'max_size': 5 * 1024 * 1024  # 5MB
    },
    'GIF': {
        'extension': ['gif'],
        'mime': 'image/gif',
        'max_size': 8 * 1024 * 1024  # 8MB
    }
}

# Document Types
DOCUMENTS = {
    'PDF': {
        'extension': ['pdf'],
        'mime': 'application/pdf',
        'max_size': 20 * 1024 * 1024  # 20MB
    },
    'WORD': {
        'extension': ['doc', 'docx'],
        'mime': ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        'max_size': 15 * 1024 * 1024  # 15MB
    }
}

# Video Types
VIDEOS = {
    'MP4': {
        'extension': ['mp4'],
        'mime': 'video/mp4',
        'max_size': 100 * 1024 * 1024  # 100MB
    },
    'WebM': {
        'extension': ['webm'],
        'mime': 'video/webm',
        'max_size': 50 * 1024 * 1024  # 50MB
    }
}