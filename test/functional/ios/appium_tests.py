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

import unittest
from time import sleep

from appium import webdriver
from appium.webdriver.applicationstate import ApplicationState
from appium.webdriver.common.mobileby import MobileBy
from helper import desired_capabilities


class AppiumTests(unittest.TestCase):
    def setUp(self):
        desired_caps = desired_capabilities.get_desired_capabilities('UICatalog.app.zip')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_lock(self):
        self.driver.lock(-1)
        try:
            self.assertTrue(self.driver.is_locked())
        finally:
            self.driver.unlock()
        self.assertFalse(self.driver.is_locked())

    def test_screen_record(self):
        self.driver.start_recording_screen()
        sleep(10)
        result = self.driver.stop_recording_screen()
        self.assertTrue(len(result) > 0)

    def test_app_management(self):
        # this only works in Xcode9+
        if float(desired_capabilities.get_desired_capabilities(
                desired_capabilities.BUNDLE_ID)['platformVersion']) < 11:
            return
        self.assertEqual(self.driver.query_app_state(desired_capabilities.BUNDLE_ID),
                         ApplicationState.RUNNING_IN_FOREGROUND)
        self.driver.background_app(-1)
        self.assertTrue(self.driver.query_app_state(desired_capabilities.BUNDLE_ID) <
                        ApplicationState.RUNNING_IN_FOREGROUND)
        self.driver.activate_app(desired_capabilities.BUNDLE_ID)
        self.assertEqual(self.driver.query_app_state(desired_capabilities.BUNDLE_ID),
                         ApplicationState.RUNNING_IN_FOREGROUND)

    def test_shake(self):
        # what can we assert about this?
        self.driver.shake()

    def test_touch_id(self):
        # nothing to assert, just verify that it doesn't blow up
        self.driver.touch_id(True)
        self.driver.touch_id(False)

    def test_toggle_touch_id_enrollment(self):
        # nothing to assert, just verify that it doesn't blow up
        self.driver.toggle_touch_id_enrollment()

    def test_hide_keyboard(self):
        self._move_to_textbox()

        el = self.driver.find_elements_by_class_name('XCUIElementTypeTextField')[0]
        el.set_value('Testing')

        el = self.driver.find_element_by_class_name('UIAKeyboard')
        self.assertTrue(el.is_displayed())

        self.driver.hide_keyboard(key_name='Done')

        self.assertFalse(el.is_displayed())

    def test_hide_keyboard_presskey_strategy(self):
        self._move_to_textbox()

        el = self.driver.find_elements_by_class_name('XCUIElementTypeTextField')[0]
        el.set_value('Testing')

        el = self.driver.find_element_by_class_name('UIAKeyboard')
        self.assertTrue(el.is_displayed())

        self.driver.hide_keyboard(strategy='pressKey', key='Done')

        self.assertFalse(el.is_displayed())

    def test_hide_keyboard_no_key_name(self):
        self._move_to_textbox()

        el = self.driver.find_elements_by_class_name('XCUIElementTypeTextField')[0]
        el.set_value('Testing')

        el = self.driver.find_element_by_class_name('UIAKeyboard')
        self.assertTrue(el.is_displayed())

        self.driver.hide_keyboard()
        sleep(10)

        # currently fails.
        self.assertFalse(el.is_displayed())

    def test_is_keyboard_shown(self):
        self._move_to_textbox()

        el = self.driver.find_elements_by_class_name('XCUIElementTypeTextField')[0]
        el.set_value('Testing')
        self.assertTrue(self.driver.is_keyboard_shown())

    def test_clear(self):
        self._move_to_textbox()

        el = self.driver.find_elements_by_class_name('XCUIElementTypeTextField')[0]

        # Verify default text
        def_text = 'Placeholder text'
        text = el.get_attribute('value')
        self.assertEqual(text, def_text)

        # Input some text, verify
        input_text = 'blah'
        el.send_keys(input_text)
        text = el.get_attribute('value')
        self.assertEqual(text, input_text)

        # Clear text, verify
        el.clear()
        text = el.get_attribute('value')
        self.assertEqual(text, def_text)

    def test_press_button(self):
        self.driver.press_button("Home")
        if float(desired_capabilities.get_desired_capabilities(
                desired_capabilities.BUNDLE_ID)['platformVersion']) < 11:
            return
        self.assertEqual(self.driver.query_app_state(desired_capabilities.BUNDLE_ID),
                         ApplicationState.RUNNING_IN_FOREGROUND)

    def _move_to_textbox(self):
        el1 = self.driver.find_element_by_accessibility_id('Sliders')
        el2 = self.driver.find_element_by_accessibility_id('Buttons')
        self.driver.scroll(el1, el2)

        # Click text fields
        self.driver.find_element_by_accessibility_id('Text Fields').click()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AppiumTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
