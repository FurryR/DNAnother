# 欢迎

欢迎使用 DNAnother!这是一个个人开发的，开源的[DNA](https://gitee.com/sharpeter/DNA)替代品。  
目前只支持 Aonly 分区。我们将努力尝试支持 A/B 式分区。  
DNAnother 比 DNA 更加人性化，同时兼顾了易用性。您可以通过安装功能读取他人模板来快速完成 ROM！  
This program was under the **LGPLv2.1** Open-Source License.此程序基于**LGPLv2.1**开源协议。

# 初次使用

## Linux/WSL

**[这里](help.md)提供了基本的使用教程。在开始使用前，请务必进行使用方法的学习。**  
在控制台输入以下内容：

```
. <(curl -L https://git.io/J0qTU)
```

## Termux

需要**虚拟 debian 系容器**环境。  
解包**需要root权限**。  
没有root权限的情况下，您可以尝试利用其它实用工具（比如Zarchiver）进行浏览（会导致权限问题所以请务必不要实际刷入）。  
请在**虚拟容器内控制台**输入以下内容：

```
. <(curl -L https://git.io/J0qTU)
```

# 相比 DNA 的缺点

**可能不支持**Android 7.0 以下的镜像。  
低强壮性。预期以外的操作**可能导致崩溃**。  
**可能不支持线刷包**。我们仍支持解包 img，但可能无法支持 super.img 的解包。  
**暂时不支持**高级操作，例如：

- 合并分段 dat  
- 分解 TWRP 备份文件  
  如果您实在是非常需要这些功能，我推荐您去使用闭源的 DNA 和 付费且闭源的 RNA。

# 相比 DNA 的优点

**完全开源**，无**任何有害代码**。  
程序本体不会修改**任何分区内**的**任何文件**(例如加入作者名)。  
界面**更加人性化**，更加**容易上手**。  
允许您**决定命令参数**来提高打包和转换的速度。  
程序本体**轻量化**。  
**支持解包 boot 和 recovery**。  
理论(只是理论)可以**移植到 Windows 代替 RNA**。  
使用**完全免费**。无论是移植到哪个平台都**完全免费**。  
(请不要违反 LGPLv3。)

# 测试通过的项目

**其他->高级转换** on MIUIGlobal 12.5.1 卡刷包  
**解压/打包** on MIUIGlobal 12.5.1 卡刷包  
**安装** on MIUIGlobal 12.5.1 卡刷包  
**调整额外参数** on N/A

# 警告

**请不要拿本软件本体或衍生软件本体去卖，也请不要相信任何售卖本软件的商家(包括 CSDN 下载)。**  
DNAnother 允许您创建插件(见帮助)，您可以自行决定插件所使用的开源协议，甚至闭源。  
为了提高/维护社区健康度，请尽可能开源来保证友好性。  
对于刷成砖、打包无法使用的情况，作者完全免责。

# 版权信息

本软件使用了数个开源软件，并且它们协议各不相同。  
为了避免协议冲突，任何使用到的开源软件的修改版本均使用和原软件包相同的协议开源（无论是否硬性要求）。  

# 反馈

本软件目前仍然处在不稳定的状态，如果遇到任何bug，请参照[bug手册](bug.md)来获得解决办法。  
找不到的情况下，请合理利用**issue**功能或点击[这里](mailto:awathefox@gmail.com)来反馈bug。

# 捐赠

没得捐赠，给那些交 pr 的好心人吧。

# 感谢

DNAnother 的诞生离不开这些软件包。  
[sdat2img](https://github.com/xpirt/sdat2img)  
[img2sdat](https://github.com/xpirt/img2sdat)  
[brotli](https://github.com/google/brotli)  
[zip](http://www.info-zip.org/Zip.html)  
[unzip](http://www.info-zip.org/UnZip.html)  
[dialog](https://invisible-island.net/dialog/dialog.html)  
[python3](https://www.python.org/)  
[git](https://git-scm.com/)  
[android-sdk-libsparse-utils](https://android.googlesource.com/platform/system/core)  
[abootimg](http://gitorious.org/ac100/abootimg)  
[img2simg](https://android.googlesource.com/platform/system/core)  
[simg2img](https://android.googlesource.com/platform/system/core)  
[payload_dumper](https://github.com/vm03/payload_dumper)
