# Dark_link
用于检测网站上面的暗链情况，原理是根据搜索所有的隐藏url，再通过获取隐藏url的源代码，去做敏感词汇过滤，敏感词库做了去重以及去掉了大量多余经常冲突的词汇。

先根据httpx爬取网站所有网页url记录，再去扫描相关的网址。

做了去重以及本站外站的显示，因为一般都是外站链接由于不维护，失效域名等出现问题多。

可优化：需要根据自身需求优化rules规则表，可以增加多线程，根据自己电脑性能，这样跑的更快，单线程实测还是太慢。

不可用于非法检测网站，作者对用户行为不承担任何责任。
