import unittest
import os

from common import SPOTIFY_REFRESH_TOKEN_DB_KEY, ARCHIVE_PLAYLIST_ID_DB_KEY
from repository import FileRepository


class TestFileRepository(unittest.TestCase):
    def delete_file_if_present(self, file):
        if os.path.isfile(file):
            os.remove(file)

    def test_ReadWriteUser_NoFile_ReturnsCorrectData(self):
        test_file = "test_repo.json"
        self.delete_file_if_present(test_file)

        # arange
        repo = FileRepository.instance(test_file)

        # act
        repo.write_user("test_id", "test_token", "test_playlist_id")
        data = repo.get_user("test_id")

        # assert
        self.assertEqual(
            data[SPOTIFY_REFRESH_TOKEN_DB_KEY], "test_token")
        self.assertEqual(
            data[ARCHIVE_PLAYLIST_ID_DB_KEY], "test_playlist_id")

    def test_ReadUser_NoFile_ReturnsEmpty(self):
        test_file = "test_repo.json"
        self.delete_file_if_present(test_file)
        repo = FileRepository.instance(test_file)

        data = repo.get_user("test_id")

        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()
