1. 到目标目录下右键，git bash here
1. 配置用户信息
>git config --global user.name xxx
>git config --global user.email xxx@xxx
* push常见用法
  * 一般格式：git push <远程主机名> <本地分支名> <远程分支名>
  * 完整：git push origin main:refs\for\main
  * git push origin main 省略了远程分支，默认和本地同名
  * git push origin : refs/for/master 省略了本地分支，等同将一个空分支push，等于删除远程分支，即git push origin --delete master
  * git push origin，如果当前分支和远程分支存在追踪关系，那么都能省略
  * git push，如果当前只有一个远程分支，那么远程主机名也能省略 
  * git push -u origin main ,当前分支和多个主机有跟踪关系，-u指定一个默认主机，这样以后就可以不加任何参数直接git push
  * 
1. 跟着github教程试试
>git init
>git add README.md
>git commit -m "first commit"
>git branch -M main
>git remote add origin https://github.com/xfjwljh/github-use.git
> git push -u origin main

然后会有登录界面，选第一个，然后进入网页登陆授权
报错：fatal: unable to access 'http://github.com/xfjwljh/github-use.git/': OpenSSL SSL_read: Connection was reset, errno 10054

解决1：git config --global http.sslVerify "false" ,没有解决
解决2：git config http.postBuffer 524288000

报错：fatal: unable to access 'http://github.com/xfjwljh/github-use.git/': Failed to connect to github.com port 443 after 21052 ms: Timed out

解决1：用ssh代替http
>git remote origin remove origin
>git remote add origin git@github.com:xfjwljh/github-use.git

报错：Connection reset by 140.82.114.3 port 22
fatal: Could not read from remote repository.Please make sure you have the correct access rights
and the repository exists.

解决1：在github账号中添加ssh key
>ssh-keygen -t rsa -C"2777192525@qq.com"

然后进入提示信息的路径中，找到id_rsa.pub,用记事本打开，复制内容
计入github，头像下面进入settings，在左边找到SSH and GPC keys 一项，新建一个ssh，标题随意，将刚才复制的内容放到下面

还是报同样的错

尝试不用git push -u origin main,而是git push
报错：fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use  git push --set-upstream origin main

还是报同样的错，淦

等了一会儿，重新push成功了，可能在github上更新ssh需要一点时间同步


# clone 一个仓库到本地
git clone http://github.com/sfjwljh/sfjwljh.git

报错：fatal: unable to access 'http://github.com/sfjwljh/sfjwljh.git/': OpenSSL SSL_read: Connection was reset, errno 10054

又输了一遍$ git config --global http.sslVerify "false"
报错：fatal: unable to access 'http://github.com/sfjwljh/sfjwljh.git/': Failed to connect to github.com port 443 after 21099 ms: Timed out

解决：不用http的连接，用git clone git@github.com:sfjwljh/sfjwljh.git,成功

# push别人的库到别人的git仓
直接 git push origin main,失败
可以从别人的仓库里先fork到自己的仓，然后clone到本地，修改add,commit,push到自己的仓中之后，在网页版中提交pull request

