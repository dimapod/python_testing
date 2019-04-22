import os.path
import tempfile
import unittest

import mock

from mock1 import rm, RemovalService, UploadService


class RmTestCase(unittest.TestCase):
    tmp_file_path = os.path.join(tempfile.gettempdir(), "tmp-testfile")

    def setUp(self):
        with open(self.tmp_file_path, "w") as f:
            f.write("Delete me!")

    def test_rm(self):
        rm(self.tmp_file_path)
        self.assertFalse(os.path.isfile(self.tmp_file_path), "Failed to remove the file.")


class RmTestCaseMock(unittest.TestCase):

    @mock.patch('mock1.os')
    def test_rm(self, mock_os):
        rm("any path")
        mock_os.remove.assert_called_with("any path")


class RmTestCaseMock2(unittest.TestCase):

    @mock.patch('mock1.os.path')
    @mock.patch('mock1.os')
    def test_should_fail_when_not_a_file(self, mock_os, mock_path):
        # given
        mock_path.isfile.return_value = False

        # when
        rm("any path")

        # then
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")

    @mock.patch('mock1.os.path')
    @mock.patch('mock1.os')
    def test_should_remove_file(self, mock_os, mock_path):
        # given
        mock_path.isfile.return_value = True

        # when
        rm("any path")

        # then
        mock_os.remove.assert_called_with("any path")


class RmServiceTestCase(unittest.TestCase):

    @mock.patch('mock1.os.path')
    @mock.patch('mock1.os')
    def test_should_fail_when_not_a_file(self, mock_os, mock_path):
        # given
        reference = RemovalService()
        mock_path.isfile.return_value = False

        # when
        reference.rm("any path")

        # then
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")

    @mock.patch('mock1.os.path')
    @mock.patch('mock1.os')
    def test_should_remove_file(self, mock_os, mock_path):
        # given
        reference = RemovalService()
        mock_path.isfile.return_value = True

        # when
        reference.rm("any path")

        # then
        mock_os.remove.assert_called_with("any path")


class UploadServiceTestCase(unittest.TestCase):

    @mock.patch.object(RemovalService, 'rm')
    def test_upload_complete_with_patch_object(self, mock_rm):
        # given
        removal_service = RemovalService()
        reference = UploadService(removal_service)

        # when
        reference.upload_complete("my uploaded file")

        # then
        mock_rm.assert_called_with("my uploaded file")
        removal_service.rm.assert_called_with("my uploaded file")

    def test_upload_complete_with_mocked_instance(self):
        # given
        mock_removal_service = mock.create_autospec(RemovalService)
        reference = UploadService(mock_removal_service)

        # when
        reference.upload_complete("my uploaded file")

        # then
        mock_removal_service.rm.assert_called_with("my uploaded file")

