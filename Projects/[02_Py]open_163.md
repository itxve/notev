# open_163

[Demo](https://github.com/SigureMo/MOOC_Downloading/blob/master/open163.py)  
[项目地址](https://github.com/SigureMo/course-crawler/blob/master/mooc/open_163.py)

## 1 从觊觎到实现
### 1.1 从xml获取视频url
测试课程：[哈佛大学公开课：计算机科学cs50](http://open.163.com/special/opencourse/cs50.html)  
话不多说，首先抓包！  
![[02_Py]open_16301.png](../Images/[02_Py]open_16301.png)  
打开一个视频，F12抓包，可以看到有一个xml的接口可以获得“url”，呃，虽然人家写着是url，但是……这根本不可读呀，而且……抓到的包里面根本木有视频呀……伤心，去查了下，发现了这个ヾ(◍°∇°◍)ﾉﾞ [如何批量获取网易公开课Request Url?](https://segmentfault.com/q/1010000007225934)
### 1.2 反编译swf
> 下面就不提供截图啦，一方面是原来反编译的文件找不到啦，另一方面是出于保护网易的版权（总这样“针对”人家有点怪不好意思的，不过自学之路上还是很感谢他的），这里主要记录下这个过程，比较一下flash与HTML5的异同（也许过几年flash就不存在了呢QAQ）  

了解了下，swf文件是flash的文件，而open_163暂时还是用flash播放视频的，据观察，这个swf类似于js，是在前端进行解释执行的，而url的解密也是在swf中进行的。

先在抓到的包里面把swf下载下来，利用SWFDecompiler对它进行反编译，然后就要在庞大的源码目录中寻找解密过程╥﹏╥

### 1.3 漫漫寻找路
我刚开始也是直接找的，到最后的结果就是……观察了下目录结构……而且因为之前搜到某个反编译swf的帖子中说看到了很多java代码，被先入为主的我居然以为这些代码是某些我没学过的高级语法……但是越看越不对劲……用var申明变量什么鬼啊，怎么是动态语言……查了下才知道这鬼东西居然是ActionScript，然后我就又去看了下这东西的基本语法（赋值啥的）

找了好久还是没找到，后来我索性做了一个文本查找脚本（很简单，应该只利用了os.walk），对某些关键词进行查找，经过几次的筛选，总算找到了有点相关的代码[](src/com/netease/openplayer/model/OpenMovieData.as)。里面大概写着获取到xml后对url进行解密的过程，明白了他是使用aes进行加密，加密密钥也在相应的文件中，所以我们只需要模拟这个过程就好。

### 1.4 AES解密
之前有在deepin上使用过Crypto，但是Windows上死活安装不上，查了下，现在是使用pycryptodome对原来的Crypto进行替代，使用pip安装即可。

根据swf源码，可以得到需要将xml中获取的16进制字符串转化为二进制字节流，这里利用bytes.fromhex(hex_string)函数即可，之后再利用aes.decrypt(bytes)便可得到解密后的字符流，最后只需要str(bytes)便可获得真正的url啦

### 1.5 组装组装！
连最复杂的解密过程都完成啦，下一步就是把各部分代码组装就好啦（虽然这里面没写……因为那些都只是最简单的爬虫过程啦），然后我们的小小open_163爬虫便做好啦！

# Reference
1. [如何批量获取网易公开课Request Url?](https://segmentfault.com/q/1010000007225934)

# 修改记录
1. 180827 Init
3. 180923 Add #1

[goto S_Note;](../README.md)

[return 0;](#open_163)