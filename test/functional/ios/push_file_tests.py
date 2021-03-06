#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest

from appium import webdriver
from helper import desired_capabilities


class PushFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        desired_caps = desired_capabilities.get_desired_capabilities('UICatalog.app.zip')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_push_file(self):
        file_name = 'test_image.jpg'
        source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file', file_name)
        destination_path = file_name

        self.driver.push_file(destination_path, source_path=source_path)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PushFileTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
