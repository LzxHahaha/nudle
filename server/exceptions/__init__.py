class UnknownImageError(Exception):
    def __init__(self, file_type='unknown'):
        self.message = 'Except png or jpeg image but receive %s' % file_type
        self.code = 415


class UnknownLibraryError(Exception):
    def __init__(self, lib_name='unknown'):
        self.message = 'No library named %s' % lib_name
        self.code = 404
