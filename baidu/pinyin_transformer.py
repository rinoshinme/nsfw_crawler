# -*- encoding: utf-8 -*-
import pypinyin

# 原文：https: // blog.csdn.net / r_coder / article / details / 79419318
# 不带声调的(style=pypinyin.NORMAL)
def hp(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


# 带声调的(默认)
def hp2(word):
    s = ''
    for i in pypinyin.pinyin(word):
        s = s + ''.join(i) + " "
    return s


if __name__ == "__main__":
    print(hp("中国中央电视台春节联欢晚会"))
    print(hp2("中国中央电视台春节联欢晚会"))
    print(hp2("长大"))
    print(hp2("长方形"))
    print(hp2("长方形123二进制"))
