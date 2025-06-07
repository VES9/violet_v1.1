import re

def clean_filename(filename):
    # 定义需要去除的非法字符的正则表达式
    illegal_chars = r'[\/\\\:\*\?"<>\|]'  # 注意正则表达式中的转义字符
    # 使用正则表达式将非法字符替换为空格
    cleaned_filename = re.sub(illegal_chars, ' ', filename)
    # 去除首尾空格，避免文件名中间出现连续空格
    cleaned_filename = cleaned_filename.strip()
    # 过滤掉不是汉字或英文字母的字符
    cleaned_filename = ''.join([char for char in cleaned_filename if char.isalpha() or '\u4e00' <= char <= '\u9fff'])
    return cleaned_filename