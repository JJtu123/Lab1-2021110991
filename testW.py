import unittest

# 导入要测试的函数
from myModuleW import process_file
from myModuleW import query_path

file_path = "E:\\Course\\Software_Engineering\\Labs\\Lab_01\\Code\\Test.txt"
process_file(file_path)

class TestQueryBridgeWords(unittest.TestCase):

    # 测试用例1：所覆盖的基本路径编号为 1。
    def test_valid_equivalence_class_1(self):
        result = query_path("lab", "the")
        expected_result = "No lab in the graph!"
        self.assertEqual(result, expected_result)

    # 测试用例2：所覆盖的基本路径编号为 2。
    def test_valid_equivalence_class_2(self):
        result = query_path("various", "cat")
        expected_result = "No cat in the graph!"
        self.assertEqual(result, expected_result)

    # 测试用例3：所覆盖的基本路径编号为 3。
    def test_valid_equivalence_class_3(self):
        result = query_path("end", "the")
        expected_result = "No path from end to the!"
        self.assertEqual(result, expected_result)

    # 测试用例4：所覆盖的基本路径编号为 4。
    def test_invalid_equivalence_class_1(self):
        result = query_path("various", "mixed")
        expected_result = "The shortest path is: ['various', 'special', 'characters', 'like', 'and', 'also', 'words', 'with', 'mixed'], and the shortest path length is 8"
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
