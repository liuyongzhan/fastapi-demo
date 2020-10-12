

class ConflictException(Exception):
    def __init__(self, err='资源已存在'):
        Exception.__init__(self, err)


class MaxLenException(Exception):
    def __init__(self, err='已超过可添加的最大限制数'):
        Exception.__init__(self, err)