# -*- coding: utf-8 -*-


import os
import shutil
import tempfile
from click.testing import CliRunner
from pip.index import InstallationCandidate, Link

from pur import pur, __version__

from . import utils
from .utils import u


class BaseTestCase(utils.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_help_contents(self):
        args = ['--help']
        result = self.runner.invoke(pur, args)
        self.assertIsNone(result.exception)
        self.assertEquals(result.exit_code, 0)
        self.assertIn('pur', u(result.output))
        self.assertIn('Usage', u(result.output))
        self.assertIn('Options', u(result.output))

    def test_version(self):
        args = ['--version']
        result = self.runner.invoke(pur, args)
        self.assertIsNone(result.exception)
        expected_output = "pur, version {0}\n".format(__version__)
        self.assertEquals(u(result.output), u(expected_output))
        self.assertEquals(result.exit_code, 0)

    def test_updates_package(self):
        tempdir = tempfile.mkdtemp()
        requirements = os.path.join(tempdir, 'requirements.txt')
        shutil.copy('tests/samples/requirements.txt', requirements)
        args = [requirements]

        with utils.mock.patch('pip.index.PackageFinder.find_all_candidates') as mock_find_all_candidates:
            project = 'flask'
            version = '0.10.1'
            link = Link('')
            candidate = InstallationCandidate(project, version, link)
            mock_find_all_candidates.return_value = [candidate]

            result = self.runner.invoke(pur, args)
            self.assertIsNone(result.exception)
            expected_output = "Updated flask: 0.9 -> 0.10.1\nAll requirements up-to-date.\n"
            self.assertEquals(u(result.output), u(expected_output))
            self.assertEquals(result.exit_code, 0)
            expected_requirements = "flask==0.10.1\nflask==12.0\n\n-r another-requirements.txt\n\n-e git://github.com/kennethreitz/inbox.py.git@551b4f44b144564504c687cebdb4c543cb8e9adf#egg=inbox\n"
            self.assertEquals(open(requirements).read(), expected_requirements)

    def test_updates_package_to_output_file(self):
        tempdir = tempfile.mkdtemp()
        output = os.path.join(tempdir, 'output.txt')
        requirements = open('tests/samples/requirements.txt').read()
        args = ['tests/samples/requirements.txt', '--output', output]

        with utils.mock.patch('pip.index.PackageFinder.find_all_candidates') as mock_find_all_candidates:
            project = 'flask'
            version = '0.10.1'
            link = Link('')
            candidate = InstallationCandidate(project, version, link)
            mock_find_all_candidates.return_value = [candidate]

            result = self.runner.invoke(pur, args)
            self.assertIsNone(result.exception)
            expected_output = "Updated flask: 0.9 -> 0.10.1\nAll requirements up-to-date.\n"
            self.assertEquals(u(result.output), u(expected_output))
            self.assertEquals(result.exit_code, 0)
            self.assertEquals(open('tests/samples/requirements.txt').read(), requirements)
