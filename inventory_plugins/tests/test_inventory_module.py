import unittest
import os
from ssh_config_plugin import InventoryModule  # Replace 'your_module' with the actual module name

class TestSSHConfigData(unittest.TestCase):

    def setUp(self):
        # Set testdir in local .ssh
        home_directory = os.path.expanduser('~')
        self.test_dir = os.path.join(home_directory, '.ssh/testdir') 

        # Instantiate the InventoryModule class
        self.inventory_module = InventoryModule()

    def test_get_ssh_config_data(self):
        # Call the function with the temporary directory
        result = self.inventory_module._get_ssh_config_data(self.test_dir)
        print(result)

        pass 
        # Expected output
        # expected = []

        # Assert that the result matches the expected output
        # self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()