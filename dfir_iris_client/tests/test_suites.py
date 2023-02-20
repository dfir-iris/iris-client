import unittest
from dfir_iris_client.tests.test_admin import AdminTest
from dfir_iris_client.tests.test_analysis_status import AnalysisStatusTest
from dfir_iris_client.tests.test_asset_type import AssetTypeTest
from dfir_iris_client.tests.test_case import CaseTest
from dfir_iris_client.tests.test_customer import CustomerTest
from dfir_iris_client.tests.test_event_categories import EventCategoryTest
from dfir_iris_client.tests.test_global_search import GlobalSearchTest
from dfir_iris_client.tests.test_ioc_types import IocTypesTest
from dfir_iris_client.tests.test_task_status import TaskStatusTest
from dfir_iris_client.tests.test_tlps import TlpTest


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_classes = [AdminTest, AnalysisStatusTest, AssetTypeTest, CaseTest, CustomerTest, EventCategoryTest,
                    GlobalSearchTest, IocTypesTest, TaskStatusTest, TlpTest]

    suites = unittest.TestSuite()
    for test_class in test_classes:
        tests = test_loader.loadTestsFromTestCase(test_class)
        suites.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suites)
