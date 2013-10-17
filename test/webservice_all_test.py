import unittest
import webservice_public_test
import webservice_factory_test
import webservice_admin_test

if __name__ == '__main__':
    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(webservice_public_test)
    suite.addTests(loader.loadTestsFromModule(webservice_factory_test))
    suite.addTests(loader.loadTestsFromModule(webservice_admin_test))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)