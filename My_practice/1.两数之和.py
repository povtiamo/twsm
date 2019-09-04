''' 
* @Author: lijiayi  
* @Date: 2019-07-02 15:03:54  
* @Last Modified by:   lijiayi  
* @Last Modified time: 2019-07-02 15:03:54  
'''
#
# @lc app=leetcode.cn id=1 lang=python3
#
# [1] 两数之和
#
# https://leetcode-cn.com/problems/two-sum/description/
#
# algorithms
# Easy (46.20%)
# Likes:    5514
# Dislikes: 0
# Total Accepted:    417.9K
# Total Submissions: 904.7K
# Testcase Example:  '[2,7,11,15]\n9'
#
# 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
# 
# 你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。
# 
# 示例:
# 
# 给定 nums = [2, 7, 11, 15], target = 9
# 
# 因为 nums[0] + nums[1] = 2 + 7 = 9
# 所以返回 [0, 1]
# 
# 
#
# class Solution:
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
#         _list=[]
#         for i in range(len(nums)):
#             if nums[i] not in _list:
#                 _list.append(target-nums[i])#插入的数据在_list中的index即为nums中与之相加的原数index
#             else:
#                 print(_list.index(nums[i]),i)
map = {}
num=[1,2,3,4,5]
target=9
for i in range(len(num)): 
    if num[i] not in map:
        map[target - num[i]] = i + 1
        print("[%s - %s]= %s + 1>>%s"%(target,num[i],i,map))
    else:
        print(map[num[i]], i + 1)