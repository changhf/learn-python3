Python 3 教程
============
python2.x中的urllib2被改为python3中的urllib.request

reload(sys)被替换为
import importlib
importlib.reload(sys)

### 异常：
[Python 问题小记](https://blog.csdn.net/u014001964/article/details/82262292)

1、unresolved reference 'unicode'
2、unresolved reference 'reload'
3、End of statement expected
在python3中使用 print(x) 代替 print x
4、unicode(sub, "UTF-8")
python3中改为sub.decode("UTF-8") 
4、python3中不需要sys.setdefaultencoding，默认编码时候unicode
也不需要unicode()