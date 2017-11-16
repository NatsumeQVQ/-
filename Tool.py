import re
class Tool:
    RemoveImg = re.compile('<img.*?>| {7}|')  #默认先删除左边img，如果左边没有，再匹配右边7个空格
    RemoveAddr = re.compile('<a.*?>|</a>')  #删除链接标签
    ReplaceLine = re.compile('<tr>|<div>|</div></p>')  #把换行的标签替换成\n
    ReplaceTD = re.compile('<td>')  # 把制表替换为\t
    ReplacePara = re.compile('<p.*?>')  # 把段落开头替换为\n并在开头加两个空格
    ReplaceBR = re.compile('<br><br>|<br>')  # 把换行和双换行替换为\n
    RemoveTag = re.compile('<.*?>')  #把其余标签去掉
    RemoveSpace = re.compile(' ')  #把空格去掉
    RemoveEnter = re.compile('\\n')
    RemoveLetter = re.compile('[a-z]')
    def replace(self,x):
        x = re.sub(self.RemoveImg,"",x)
        x = re.sub(self.RemoveAddr,"",x)
        x = re.sub(self.ReplaceLine,"",x)
        x = re.sub(self.ReplaceTD,"",x)
        x = re.sub(self.ReplacePara,"",x)
        x = re.sub(self.ReplaceBR,"",x)
        x = re.sub(self.RemoveTag,"",x)
        x = re.sub(self.RemoveSpace,"",x)
        x = re.sub(self.RemoveEnter,"",x)
        x = re.sub(self.RemoveLetter,'',x)
        return x