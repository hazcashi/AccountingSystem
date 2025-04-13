import unittest
from unittest.mock import patch, mock_open
from collections import defaultdict
import io
import sys

from accountingSystem import (
    load_transactions,
    show_total_expenses,
    show_all_transactions,
    show_expenses_on_date,
    show_daily_average_expenses,
    main
)

class TestAccountingSystemUnit(unittest.TestCase):
    """
    這個測試類別包含了對所有函式的單元測試 (Unit Tests)。
    Unit Test Planning 耗時: 50 分鐘
    Docstring writing 耗時: 15 分鐘
    Code writing 耗時: 85 分鐘
    """

    def test_load_transactions(self):
        """
        Test Name: test_load_transactions
        Description:
            測試 load_transactions 是否能正確讀取並解析檔案內容。
        Args:
            None
        Returns:
            None
        """
        mock_file_data = """userA 20230101 100
userA 20230102 200
userB 20230201 300
"""
        with patch("builtins.open", mock_open(read_data=mock_file_data)):
            result = load_transactions("fakefile.txt")

        self.assertIn("userA", result)
        self.assertIn("userB", result)
        self.assertEqual(len(result["userA"]), 2)
        self.assertEqual(len(result["userB"]), 1)
        self.assertEqual(result["userA"][0], ("20230101", 100))
        self.assertEqual(result["userA"][1], ("20230102", 200))
        self.assertEqual(result["userB"][0], ("20230201", 300))

    def test_show_total_expenses(self):
        """
        Test Name: test_show_total_expenses
        Description:
            測試 show_total_expenses 是否能正確顯示指定帳號的總花費。
        Args:
            None
        Returns:
            None
        """
        transactions = {
            "userA": [("20230101", 100), ("20230102", 200)]
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output

        show_total_expenses(transactions, "userA")

        sys.stdout = sys.__stdout__
        output_value = captured_output.getvalue().strip()

        self.assertIn("300", output_value)

    def test_show_all_transactions(self):
        """
        Test Name: test_show_all_transactions
        Description:
            測試 show_all_transactions 是否能正確顯示指定帳號的所有交易明細。
        Args:
            None
        Returns:
            None
        """
        transactions = {
            "userA": [("20230102", 200), ("20230101", 100)]
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output

        show_all_transactions(transactions, "userA")

        sys.stdout = sys.__stdout__
        output_value = captured_output.getvalue()

        self.assertIn("20230101: 100", output_value)
        self.assertIn("20230102: 200", output_value)

    def test_show_expenses_on_date(self):
        """
        Test Name: test_show_expenses_on_date
        Description:
            測試 show_expenses_on_date 是否能正確顯示指定日期的花費總額。
        Args:
            None
        Returns:
            None
        """
        transactions = {
            "userA": [("20230101", 100), ("20230101", 150), ("20230102", 200)]
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output

        show_expenses_on_date(transactions, "userA", "20230101")

        sys.stdout = sys.__stdout__
        output_value = captured_output.getvalue()

        self.assertIn("250", output_value)

    def test_show_expenses_on_date_invalid_date(self):
        """
        Test Name: test_show_expenses_on_date_invalid_date
        Description:
            測試在日期格式錯誤的情況下 show_expenses_on_date 是否能顯示錯誤訊息。
        Args:
            None
        Returns:
            None
        """
        transactions = {
            "userA": [("20230101", 100)]
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output

        show_expenses_on_date(transactions, "userA", "2023-01-01")

        sys.stdout = sys.__stdout__
        output_value = captured_output.getvalue()
        self.assertIn("Invalid date format", output_value)

    def test_show_daily_average_expenses(self):
        """
        Test Name: test_show_daily_average_expenses
        Description:
            測試 show_daily_average_expenses 是否能正確顯示指定月份的日平均花費。
        Args:
            None
        Returns:
            None
        """
        transactions = {
            "userA": [("20230101", 100), ("20230101", 50),
                      ("20230102", 200), ("20230201", 300)]
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output

        show_daily_average_expenses(transactions, "userA", "202301")

        sys.stdout = sys.__stdout__
        output_value = captured_output.getvalue()
        self.assertIn("175.00", output_value)

    def test_show_daily_average_expenses_invalid_month(self):
        """
        Test Name: test_show_daily_average_expenses_invalid_month
        Description:
            測試在月份格式錯誤的情況下，show_daily_average_expenses 是否能顯示錯誤訊息。
        Args:
            None
        Returns:
            None
        """
        transactions = {
            "userA": [("20230101", 100)]
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output

        show_daily_average_expenses(transactions, "userA", "2023-01")

        sys.stdout = sys.__stdout__
        output_value = captured_output.getvalue()
        self.assertIn("Invalid month format", output_value)


class TestAccountingSystemIntegration(unittest.TestCase):
    """
    這個測試類別包含了對系統整體流程的整合測試 (Integration Tests)。
    Integration Test Planning 耗時: 45 分鐘
    Docstring writing 耗時: 15 分鐘
    Code writing 耗時: 50 分鐘
    """

    @patch('builtins.input', side_effect=[
        'userA',
        'A',
        'Q',
        'Q'
    ])
    def test_integration_flow_total_expenses(self, mock_input):
        """
        Test Name: test_integration_flow_total_expenses
        Description:
            測試使用者進入系統後，執行「顯示總花費 (A)」功能再離開的整合流程。
        Args:
            mock_input (unittest.mock.MagicMock): 模擬使用者輸入
        Returns:
            None
        """
        mock_data = """userA 20230101 100
userA 20230102 200
userB 20230201 300
"""
        with patch("builtins.open", mock_open(read_data=mock_data)):
            captured_output = io.StringIO()
            sys.stdout = captured_output

            main()

            sys.stdout = sys.__stdout__
            output_value = captured_output.getvalue()

        self.assertIn("Total expenses for userA: 300", output_value)

    @patch('builtins.input', side_effect=[
        'xyz',
        'userB',
        'B',
        'Q',
        'Q'
    ])
    def test_integration_flow_show_all_transactions(self, mock_input):
        """
        Test Name: test_integration_flow_show_all_transactions
        Description:
            測試使用者先輸入錯誤 ID，再重新輸入正確 ID 後，執行「顯示所有交易(B)」功能的整合流程。
        Args:
            mock_input (unittest.mock.MagicMock): 模擬使用者輸入
        Returns:
            None
        """
        mock_data = """userA 20230101 100
userB 20230102 200
userB 20230103 300
"""
        with patch("builtins.open", mock_open(read_data=mock_data)):
            captured_output = io.StringIO()
            sys.stdout = captured_output

            main()

            sys.stdout = sys.__stdout__
            output_value = captured_output.getvalue()

        self.assertIn("Invalid ID. Try again.", output_value)
        self.assertIn("20230102: 200", output_value)
        self.assertIn("20230103: 300", output_value)


if __name__ == '__main__':
    unittest.main()
