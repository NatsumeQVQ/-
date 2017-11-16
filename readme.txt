1.使用时将zhihu.py中的base_url改为搜索页面的request url，并将'setoff='后面的数字改为'{}'(不包括引号)即可使用。

2.me.py和zhuanlan.py的功能都是抓取专栏文章信息，由于前后两次爬取网页结构有所变动，所以写了两个专栏爬虫。

3.Request URL的获取方法：用chrome打开网页，右击空白—检查，上方标签点击Network，二级标签点击XHR，下拉找到更多，点击更多就可以看到前缀是search的文件点击就可以看到Request URL。

4.Project Interpreter：Python 3.6.3