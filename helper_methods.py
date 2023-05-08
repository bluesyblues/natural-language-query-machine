import os
def make_dirs(dirpath: str):
    """해당하는 경로가 디렉토리인지 확인해,
    존재하는 디렉토리가 아니라면 해당 경로에 해당하는 디렉토리를 만드는 함수.

    Args:
        dirpath: 확인하고자 하는 경로. 디렉토리에 해당하는 포맷으로 들어와야 한다.
    """
    try:
        os.makedirs(dirpath)
    except OSError:
        if not os.path.isdir(dirpath):
            raise