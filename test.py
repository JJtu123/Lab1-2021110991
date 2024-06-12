import unittest

# 导入要测试的函数
from myModule import process_file
from myModule import query_bridge_words

file_path = "E:\\Course\\Software_Engineering\\Labs\\Lab_01\\Code\\Test.txt"
process_file(file_path)

class TestQueryBridgeWords(unittest.TestCase):

    # 有效等价类测试用例1：word1 和 word2 都存在于图中，并且存在桥接词。
    def test_valid_equivalence_class_1(self):
        result = query_bridge_words("quick", "dog")
        expected_result = "The bridge words from \"quick\" to \"dog\" are: \"and\""
        self.assertEqual(result, expected_result)

    # 有效等价类测试用例2：word1 和 word2 都存在于图中，但不存在桥接词。
    def test_valid_equivalence_class_2(self):
        result = query_bridge_words("brown", "test")
        expected_result = "No bridge words from \"brown\" to \"test\"!"
        self.assertEqual(result, expected_result)

    # 有效等价类测试用例3：word1 和 word2 有一个或两个不存在于图中。
    def test_valid_equivalence_class_3(self):
        result = query_bridge_words("apple", "dog")
        expected_result = "No \"apple\" or \"dog\" in the graph!"
        self.assertEqual(result, expected_result)

    # 无效等价类测试用例1：word1 和 word2 均为空字符串。
    def test_invalid_equivalence_class_1(self):
        result = query_bridge_words("", "")
        expected_result = "No \"\" or \"\" in the graph!"
        self.assertEqual(result, expected_result)

    # 无效等价类测试用例2：word1 或 word2 为空字符串，另一个为非空字符串。
    def test_invalid_equivalence_class_2(self):
        result = query_bridge_words("", "dog")
        expected_result = "No \"\" or \"dog\" in the graph!"
        self.assertEqual(result, expected_result)

    # 无效等价类测试用例3：word1 和 word2 都为非空字符串，但不合法。
    def test_invalid_equivalence_class_3(self):
        result = query_bridge_words("12quick", "dog!")
        expected_result = "No \"12quick\" or \"dog!\" in the graph!"
        self.assertEqual(result, expected_result)

    # 无效等价类测试用例4：word1 和 word2 为相同单词。
    def test_invalid_equivalence_class_4(self):
        result = query_bridge_words("quick", "quick")
        expected_result = "No bridge words from \"quick\" to \"quick\"!"
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
