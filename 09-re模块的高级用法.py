import re

# search : 根据正则表达式查找指定数据， 提示：只查找一次
# 1. 正则
# 2. 要匹配的字符串
match_obj = re.search("\d+", "苹果10个 鸭梨5个")
if match_obj:
    print(match_obj.group(), type(match_obj.group()))
else:
    print("匹配失败")

# match_obj = re.match("苹果(\d+)个 鸭梨(\d+)个", "苹果10个 鸭梨5个")
# if match_obj:
#     print(match_obj.group(1))
# else:
#     print("匹配失败")

# findall:  根据正则表达式查找指定数据， 提示：可以查找多个
# 1. 正则
# 2. 要匹配的字符串
result = re.findall("\d+", "苹果10个 鸭梨5个")
print(result)

# 1. 正则
# 2. 替换后的内容
# 3. 要匹配的字符串
# 4. count:0,默认是0表示根据正则表达式全部替换
result = re.sub("\d+", "100", "评论数:10 赞数:20", count=1)
print(result)

# 替换数据的函数
def replace_str(match_obj):
    # 获取匹配结果
    result = match_obj.group()
    value = int(result) + 1
    # 提示： 返回的数据必须是字符串
    return str(value)

# 替换函数的参数不需要程序要进行传参，有解释器自动传入
result = re.sub("\d+", replace_str, "评论数:50")
print(result)


my_str = "貂蝉,西施:王昭君,杨玉环"
# 1. 正则
# 2. 要匹配的字符串
# 3. maxsplit:0 根据正则表达式全部分割
# maxsplit=1 只分割一次
result = re.split(",|:", my_str, maxsplit=1)
print(result)