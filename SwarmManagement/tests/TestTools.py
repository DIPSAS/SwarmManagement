import os


TEST_SAMPLE_FOLDER = 'example'


def ChangeToSampleFolderAndGetCwd():
    cwd = os.getcwd()
    os.chdir(TEST_SAMPLE_FOLDER)
    return cwd