#!/usr/bin/env python3
#coding=utf-8
#copyright (c) 2021 awathefox.
#This program was under the LGPLv2.1 license.
import os
import subprocess
import sys
import shutil
import math
#dialog begin
def choice(run,default=""): # run=['title','menu',['title','obj'],['title','obj'],...]
  cmd="dialog --title \""+run[0]+"\" --default-item \""+default+"\" --menu \""+run[1]+"\" 0 0 0 "
  s=2
  while s < len(run):
    cmd+=run[s][0]+" \""+run[s][1]+"\" "
    s=s+1
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def inputbox(title,msg,default=""):
  cmd="dialog --title \""+title+"\" --inputbox \""+msg+"\" 0 0 \""+default+"\""
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def textbox(title,file):
  cmd="dialog --title \""+title+"\" --textbox \""+file+"\" 0 0"
  os.system(cmd)
  return
def fselect(title,dir=""):
  cmd="dialog --title \""+title+"\" --fselect \""+dir+"\" 0 0"
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def dselect(title,dir=""):
  cmd="dialog --title \""+title+"\" --dselect \""+dir+"\" 0 0"
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def mulchoice(run): #run=['title','menu',['title','obj'],['title','obj'],...]
  cmd="dialog --title \""+run[0]+"\" --checklist \""+run[1]+"\" 0 0 "+str(len(run[2:]) if len(run[2:]) < 5 else 5)+" "
  s=2
  while s < len(run):
    cmd+=run[s][0]+" \""+run[s][1]+"\" "+str(s-1)+" "
    s=s+1
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode().split(' ')]
def msg(title,msg):
  cmd="dialog --title \""+title+"\" --msgbox \""+msg+"\" 0 0"
  os.system(cmd)
  return
def infobox(title,msg):
  cmd="dialog --title \""+title+"\" --infobox \""+msg+"\" 10 50"
  os.system(cmd)
  return
def progress(title,msg,percent):
  cmd="echo "+str(percent)+" | dialog --title \""+title+"\" --gauge \""+msg+"\" 10 50 "+str(percent)
  os.system(cmd)
  return
def yesno(title,msg):
  cmd="dialog --title \""+title+"\" --yesno \""+msg+"\" 0 0"
  return os.system(cmd)
def exitmenu():
  os.system("clear")
  exit(0)
CHOICE_OK=0
CHOICE_NO=1
CHOICE_EXIT=255
#dialog end

#convert begin
def gettype(path):
  x=subprocess.run("file -b "+path,shell=True,stdout=subprocess.PIPE)
  return x.stdout.decode()
#br<->dat begin
def br2dat(source,output):
  os.system("brotli -d -o {0} {1}".format(output,source))
def dat2br(source,output,ext_arg):
  os.system("brotli {0} -o {1} {2}".format(ext_arg,output,source))
#br<->dat end

#dat<->img begin
def dat2img(list,source,output):
  os.system("python3 {0}/bin/sdat2img/sdat2img.py {1} {2} {3} >/dev/null".format(sys.path[0],list,source,output))
def img2dat(source,output,prefix):
  if gettype(source).startswith("Android sparse image"):
    os.system("python3 {0}/bin/img2sdat/img2sdat.py -v 4 {1} -p {2} -o {3} >/dev/null".format(sys.path[0],source,prefix,output))
  else:
    os.system("python3 {0}/bin/rimg2sdat/rimg2sdat.py -v 4 {1} -p {2} -o {3} >/dev/null".format(sys.path[0],source,prefix,output))
#dat<->img end

#img<->dir begin
def unpackimg(source,output):
  if gettype(source).startswith("Android bootimg"):
    os.chdir("temp")
    os.mkdir("abootimg")
    os.chdir("..")
    shutil.copy(source,"temp/abootimg/abootimg.tmp.img")
    os.chdir("temp/abootimg")
    os.system("abootimg -x abootimg.tmp.img >/dev/null")
    os.remove("abootimg.tmp.img")
    os.system("abootimg-unpack-initrd initrd.img 2>/dev/null")
    os.chdir("../..")
    os.system("cp -r temp/abootimg/. "+output)
    shutil.rmtree("temp/abootimg")
  else:
    if gettype(source).startswith("Android sparse image"):
      os.system("simg2img {0} temp/output.tmp.img > /dev/null")
      source="temp/output.tmp.img"
    os.system("mount -o ro {0} mount".format(source))
    os.system("cp -r mount/. {0}".format(output))
    os.system("umount mount")
    if source=="temp/output.tmp.img":
      os.remove(source)
def packimg(source,output,sparseimg=False):
  if os.path.exists(source+"/bootimg.cfg"):
    os.system("cp -r "+source+" temp/abootimg")
    os.chdir("temp/abootimg")
    if os.path.exists("ramdisk"):
      os.system("abootimg-pack-initrd initrd.new.img ramdisk/ >/dev/null")
    else:
      shutil.copyfile("initrd.img","initrd.new.img")
    os.system("abootimg --create abootimg.tmp.img -k zImage -r initrd.new.img >/dev/null".format(output))
    os.chdir("../..")
    shutil.copyfile("temp/abootimg/abootimg.tmp.img",output)
    shutil.rmtree("temp/abootimg")
    return os.path.getsize(output)
  else:
    os.system("dd if=/dev/zero of=temp/output.tmp.img bs=GiB count={1} 2>/dev/null".format(output,math.ceil(dirsize(source)*1.1/1024/1024/1024)))
    os.system("mkfs.ext4 temp/output.tmp.img >/dev/null".format(output))
    os.system("mount -o rw temp/output.tmp.img mount".format(output))
    os.system("cp -r {0}/. mount".format(source))
    os.system("umount mount")
    if sparseimg:
      os.system("img2simg temp/output.tmp.img {0}".format(output))
      os.remove("temp/output.tmp.img")
    else:
      shutil.move("temp/output.tmp.img",output)
    return os.path.getsize(output) #返回sparse_img的size 用于更新
#img<->dir end

#payload->imgs begin
def payload_partitions(file):
  x=subprocess.run("python3 {0}/bin/payload_dumper/partget.py {1}".format(sys.path[0],file),shell=True,stdout=subprocess.PIPE)
  r=x.stdout.decode().split("\n")
  for i in range(len(r)):
    if r[i]=='':
      del r[i]
  return r
def extract_payload(payload,output,images=None):
  if images==None:
    os.system("python3 {0}/bin/payload_dumper/payload_dumper.py {1} --out {2}".format(sys.path[0],payload,output))
  else:
    os.system("python3 {0}/bin/payload_dumper/payload_dumper.py {1} --out {2} --images {3}".format(sys.path[0],payload,output,",".join(images)))
#payload->imgs end

#convert end

#temp begin
def cleartemp():
  shutil.rmtree("temp",True)
  os.mkdir("temp")
def cleartarget():
  shutil.rmtree("target",True)
  os.mkdir("target")
def clearconv():
  shutil.rmtree("conv/",True)
  os.mkdir("conv")
def dirsize(dir):
  size=0
  for root,dirs,files in os.walk(dir):
    for name in files:
      f=os.path.join(root,name)
      if os.path.islink(f):
        size+=100
      elif os.path.isdir(f):
        size+=dirsize(f)
      elif os.path.isfile(f):
        size+=os.path.getsize(f)
  return size
#temp end
zip_ext_arg=""
bro_ext_arg="-1"
def convert(path,op):
  global bro_ext_arg
  global zip_ext_arg
  if op=='img2dat':
    img2dat(path,'conv/output.new.dat','output')
    if path.startswith('conv/'):
      shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    return 'conv/output.new.dat'
  elif op=='dat2img':
    while 1:
      if not path.startswith('conv/') or (path.endswith(".dat") and (not os.path.exists("conv/output.transfer.list"))):
        s=fselect("选择 "+path.split("/")[-1].split(".")[0]+".transfer.list")
      else:
        s=[CHOICE_OK,'conv/output.transfer.list']
      if s[0]!=CHOICE_OK:
        if yesno("高级转换","确实要取消转换吗?")==CHOICE_OK:
          clearconv()
          return ''
      elif os.path.exists(s[1]) and os.path.isfile(s[1]) and s[1].endswith(".list"):
        infobox("高级转换","正在处理文件,请稍等...")
        dat2img(s[1],path,'conv/output.img')
        if path.startswith('conv/'):
          shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
        return 'conv/output.img'
      else:
        msg("高级转换","无法读取文件。")
  elif op=='br2dat':
    br2dat(path,'conv/output.new.dat')
    if path.startswith('conv/'):
      shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    return 'conv/output.new.dat'
  elif op=='dat2br':
    dat2br(path,'conv/output.new.dat.br',bro_ext_arg)
    if path.startswith('conv/'):
      shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    return 'conv/output.new.dat.br'
  elif op=='packimg':
    packimg(path,'conv/output.img',True)
    if path.startswith('conv/'):
      shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    return 'conv/output.img'
  elif op=='unpackimg':
    unpackimg(path,'conv/')
    if path.startswith('conv/'):
      shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    return 'conv/'
  elif op=='cp':
    shutil.copy(path,'conv/')
    if path.startswith('conv/'):
      shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    return 'conv/'
  elif op=='extract_payload':
    extract_payload(path,"conv/")
    return 'conv/'
def highconv():
  infobox("请稍等","正在预准备")
  cleartemp()
  if yesno("高级转换","此功能会清理上一次的转换文件。\\n确实要这样做吗?")==CHOICE_OK:
    infobox("请稍等","正在清理 conv")
    clearconv()
    conv={
      'img':{
        'dat':['img2dat'],
        'br':['img2dat','dat2br'],
        'dir':['unpackimg'],
        'img':['cp'],
      },
      'br':{
        'dat':['br2dat'],
        'br':['cp'],
        'dir':['br2dat','dat2img','unpackimg'],
        'img':['br2dat','dat2img'],
      },
      'dat':{
        'dat':['cp'],
        'br':['dat2br'],
        'dir':['dat2img','unpackimg'],
        'img':['dat2img'],
      },
      'dir':{
        'dat':['packimg','dat2br'],
        'br':['packimg','img2dat','dat2br'],
        'dir':['cp'],
        'img':['packimg'],
      },
      'bin':{
        'img':['extract_payload'],
        'bin':['cp']
      }
    }
    x=inputbox("高级转换","输入起始和目标，将自动计算转换路径。\\n支持的格式:br,dat,img,dir,bin\\n语法:原格式->目标格式")
    if x[0]!=CHOICE_OK:
      return None
    else:
      a=x[1].split("->")
      if len(a)<2 or conv[a[0]]==None or conv[a[0]][a[1]]==None:
        msg("高级转换","原/目标格式错误或无法转换。")
      q=fselect("选择原文件")
      if q[0]!=CHOICE_OK:
        return None
      elif os.path.exists(q[1]) and (q[1].endswith("."+a[0]) or (os.path.isdir(q[1]) and a[0]=="dir")):
        path=q[1]
        for x in range(len(conv[a[0]][a[1]])):
          progress("高级转换","正在执行 "+conv[a[0]][a[1]][x]+" ["+str(x)+"/"+str(len(conv[a[0]][a[1]]))+"]",round((x/len(conv[a[0]][a[1]]))*100))
          path=convert(path,conv[a[0]][a[1]][x])
          if path=="":
            msg("高级转换","转换失败。")
            break
        if path=="":
          return None
        else:
          msg("高级转换","完成。\\n目标已保存在 "+path+"。")
      else:
        msg("高级转换","文件(夹)发生错误。")
        return None
def rom():
  global bro_ext_arg
  global zip_ext_arg
  if os.path.exists("base") and os.path.isdir("base"):
    while 1:
      ch=choice([
        "选择",
        "选择您要对这个项目进行的操作。",
        ["1","解压"],
        ["2","安装"],
        ["3","打包"],
        ["4","终端"],
        ["5","其他"],
        ["6","退出"],
      ])[1]
      if ch=='' or ch=='6':
        exitmenu()
      elif ch=='1':
        f=[
          '确认',
          '请选择要解压的文件',
        ]
        infobox("DNAnother","正在列出清单")
        for o in os.listdir("base"):
          s=list(os.path.splitext(o))[1][1:]
          w=gettype("base/"+o)
          if not os.path.isfile("base/"+o):
            continue
          elif o.endswith(".img") and (w.startswith("Android bootimg") or w.startswith("Android sparse image") or w.startswith("Linux rev 1.0 ext2 filesystem data")):
            f.append([o,s])
          elif o.endswith(".br"):
            f.append([o,s])
          elif o.endswith(".dat") and not o.endswith(".patch.dat"):
            f.append([o,s])
          elif o.endswith(".bin"):
            f.append([o,s])
        if len(f)<3:
          msg("DNAnother","没有可以用于解压的项目。")
          continue
        x=mulchoice(f)
        infobox("DNAnother","正在预准备")
        cleartemp()
        if x[0]==CHOICE_OK and x[1]!=['']:
          x=x[1]
          fail=False
          progress("DNAnother","检查清单中",0)
          for i in x:
            z=os.path.splitext(i)
            if z[1]==".br":
              progress(i,"正在执行 br2dat [1/3]",round(1/6*100))
              br2dat("base/{0}".format(i),"temp/{0}.tmp.dat".format(i))
              progress(i,"正在执行 dat2img [2/3]",round(2/6*100))
              while 1:
                if not os.path.exists("base/{0}.transfer.list".format(i.split(".")[0])):
                  s=fselect("选择 "+i.split(".")[0]+".transfer.list")
                else:
                  s=[CHOICE_OK,'base/{0}.transfer.list'.format(i.split(".")[0])]
                if s[0]!=CHOICE_OK:
                  if yesno(i,"确实要取消转换吗?")==CHOICE_OK:
                    cleartemp()
                    fail=True
                    break
                elif os.path.exists(s[1]) and os.path.isfile(s[1]) and s[1].endswith(".list"):
                  infobox(i,"正在处理文件,请稍等...")
                  dat2img(s[1],"temp/{0}.tmp.dat".format(i),"temp/{0}.tmp.img".format(i))
                  break
                else:
                  msg(i,"无法读取文件。")
              progress(i,"正在执行 dat2img [2/3]",round(3/6*100))
              os.remove("temp/{0}.tmp.dat".format(i))
              progress(i,"正在执行 unpackimg [3/3]".format(i),round(4/6*100))
              unpackimg("temp/{0}.tmp.img".format(i),"target/{0}".format(i.split(".")[0]))
              progress(i,"正在执行 unpackimg [3/3]",round(5/6*100))
              os.remove("temp/{0}.tmp.img".format(i))
              progress(i,"过程完成",100)
            elif z[1]==".dat":
              progress(i,"正在执行 dat2img [1/2]",round(1/4*100))
              while 1:
                if not os.path.exists("base/{0}.transfer.list".format(i.split(".")[0])):
                  s=fselect("选择 "+i.split(".")[0]+".transfer.list")
                else:
                  s=[CHOICE_OK,'base/{0}.transfer.list'.format(i.split(".")[0])]
                if s[0]!=CHOICE_OK:
                  if yesno(i,"确实要取消转换吗?")==CHOICE_OK:
                    cleartemp()
                    fail=True
                    break
                elif os.path.exists(s[1]) and os.path.isfile(s[1]) and s[1].endswith(".list"):
                  infobox(i,"正在处理文件,请稍等...")
                  dat2img(s[1],"base/{0}".format(i),"temp/{0}.tmp.img".format(i))
                else:
                  msg(i,"无法读取文件。")
              progress(i,"正在执行 unpackimg [2/2]".format(i),round(2/4*100))
              unpackimg("temp/{0}.tmp.img".format(i),"target/{0}".format(i.split(".")[0]))
              progress(i,"正在执行 unpackimg [2/2]",round(3/4*100))
              os.remove("temp/{0}.tmp.img".format(i))
              progress(i,"过程完成",100)
            elif z[1]==".img":
              progress(i,"正在执行 unpackimg [1/1]".format(i),round(1/2*100))
              unpackimg("base/{0}".format(i),"target/{0}".format(i.split(".")[0]))
              progress(i,"过程完成",100)
            elif z[1]==".bin":
              if yesno("警告 - "+i,"确实要解包payload.bin吗？\\n打包操作将无法进行或生成错误。")!=CHOICE_OK:
                continue
              infobox(i,"正在列出分区...")
              a=payload_partitions("base/"+i)
              p=[
                i,
                "请选择要解压的分区",
              ]
              for d in range(len(a)):
                p.append([str(d+1),a[d]])
              p=mulchoice(p)
              if p[0]==CHOICE_OK:
                p=p[1]
                infobox(i,"正在检查情报...")
                fin=[]
                for l in p:
                  fin.append(a[int(l)-1])
                progress(i,"正在执行 extract_payload [1/1]",100)
                extract_payload("base/"+i,"temp/",fin)
                for g in os.listdir("temp/"):
                  c=gettype("temp/"+g)
                  if c.startswith("Android sparse image") or c.startswith("Android bootimg") or c.startswith("Linux rev 1.0 ext2 filesystem data"):
                    progress(i+"->"+g,"正在执行 unpackimg [1/1]",50)
                    unpackimg("temp/{0}".format(g),"target/{0}".format(g.split(".")[0]))
                    progress(i+"->"+g,"正在执行 unpackimg [1/1]",100)
                    os.remove("temp/{0}".format(g))
                    progress(i+"->"+g,"过程完成",100)
                  else:
                    progress(i+"->"+g,"正在执行 cp [1/1]",50)
                    shutil.copy("temp/{0}".format(g),"target/")
                    progress(i+"->"+g,"正在执行 cp [1/1]",100)
                    os.remove("temp/{0}".format(g))
                    progress(i+"->"+g,"过程完成",100)
            else:
              fail=True
              break
          if fail:
            msg("DNAnother","转换失败。\\n已转换成功的将被保留。")
          else:
            msg("DNAnother","完成。")
      elif ch=='2':
        infobox("DNAnother","正在预准备")
        cleartemp()
        file=fselect("选择补丁包[.zip]","/")
        progress("安装中","准备中...",0)
        if file[0]==CHOICE_OK and os.path.exists(file[1]) and os.path.isfile(file[1]) and file[1].endswith(".zip"):
          progress("安装中","正在解压缩补丁...",0)
          os.system("unzip -d temp \""+file[1].replace("\"","\\\"")+"\"")
          progress("安装中","正在安装补丁...",50)
          s_backup=os.getcwd()
          os.chdir("target")
          os.system("bash ../temp/install.sh")
          os.chdir(s_backup)
          progress("安装中","正在清理临时文件")
          cleartemp()
          msg("安装补丁","完成。")
          input()
        elif file[0]==CHOICE_OK:
          msg("错误","文件不正确。")
      elif ch=='3':
        infobox("DNAnother","正在预准备")
        cleartemp()
        if yesno("警告","是否开始打包？\\n操作可能需要5分钟或更久。")==CHOICE_OK:
          progress("DNAnother","准备中",0)
          for i in os.listdir("target"):
            progress(i,"正在检查信息".format(i),0)
            if os.path.isfile("target/"+i):
              progress(i,"正在执行 cp [1/1]",100)
              os.system("cp target/"+i+" temp/")
            elif os.path.exists("target/"+i+"/bootimg.cfg"):
              progress(i,"正在执行 packimg [1/1]".format(i),100)
              packimg("target/{0}".format(i),"temp/{0}.img".format(i))
              progress(i,"完成".format(i),100)
            else:
              progress(i,"正在执行 packimg [1/3]".format(i),round(1/6*100))
              packimg("target/{0}".format(i),"temp/{0}.img".format(i),True)
              progress(i,"正在执行 img2dat [2/3]".format(i),round(2/6*100))
              img2dat("temp/{0}.img".format(i),"temp",i)
              progress(i,"正在执行 img2dat [2/3]".format(i),round(3/6*100))
              os.remove("temp/{0}.img".format(i))
              progress(i,"正在执行 dat2br [3/3]".format(i),round(4/6*100))
              dat2br("temp/{0}.new.dat".format(i),"temp/{0}.new.dat.br".format(i),bro_ext_arg)
              progress(i,"正在执行 dat2br [3/3]".format(i),round(5/6*100))
              os.remove("temp/{0}.new.dat".format(i))
              progress(i,"完成".format(i),100)
          progress("DNAnother","准备中",0)
          progress("DNAnother","复制文件...",50)
          os.system("cp -r base/* temp")
          progress("DNAnother","复制完成...",50)
          progress("DNAnother","准备中",0)
          progress("DNAnother","打包中",0)
          os.chdir("temp")
          os.system("zip ../update.zip -rq * "+zip_ext_arg)
          os.chdir("..")
          progress("DNAnother","打包完成",100)
          infobox("DNAnother","正在清理临时文件...")
          cleartemp()
          msg("DNAnother","包已经生成为 update.zip。\\n请查看项目根目录。")
      elif ch=='4':
        os.system("clear")
        s_backup=os.getcwd()
        os.chdir("target")
        print("您现在正在 target 文件夹内。")
        print("如果您需要操作指定分区，只需输入：cd [分区名]")
        print("DNAnother 感谢您的使用。")
        print("注意:您需要手动回到普通用户。")
        print("以root账户操作ROM包可能导致权限错误。")
        os.system("bash")
        os.chdir(s_backup)
      elif ch=='5':
        while 1:
          ch=choice([
            "其他",
            "这里列出了一些高级操作。\\n不当使用将导致项目损坏。",
            ["1","清空 temp"],
            ["2","清空 target"],
            ["3","高级转换"],
            ["4","调整额外参数"],
            ["5","关于"],
            ["6","返回"],
          ])[1]
          if ch=='' or ch=='6':
            break
          elif ch=='1':
            infobox("请稍等","正在清空 temp")
            cleartemp()
          elif ch=='2':
            if yesno("警告","此操作会删除最后一次打包后所做的任何更改。\\n就算这样也要继续吗？")==CHOICE_OK:
              infobox("请稍等","正在清空 target")
              cleartarget()
          elif ch=='3':
            highconv()
          elif ch=='4':
            ch=choice([
              "调整额外参数",
              "请选择要设定的程序。",
              ["1","zip"],
              ["2","brotli"]
            ])
            if ch[0]==CHOICE_OK:
              if ch[1]=='1':
                x=inputbox("调整额外参数","请输入zip的额外参数:",zip_ext_arg)
                if x[0]==CHOICE_OK:
                  zip_ext_arg=x[1]
                  msg("调整额外参数","变更已保存。")
              if ch[1]=='2':
                x=inputbox("调整额外参数","请输入brotli的额外参数:",bro_ext_arg)
                if x[0]==CHOICE_OK:
                  bro_ext_arg=x[1]
                  msg("调整额外参数","变更已保存。")
          elif ch=='5':
            if not os.path.exists("{0}/about.txt".format(sys.path[0])) or not os.path.isfile("{0}/about.txt".format(sys.path[0])):
              msg("错误","找不到关于文档。")
            else:
              textbox("关于","{0}/about.txt".format(sys.path[0]))
  else:
    msg("错误","发生错误，请检查您的项目。")
    exitmenu()
if os.geteuid() != 0:
  msg("中止","请尝试用sudo再试一遍。")
  exitmenu()
while 1:
  project_path=dselect("打开项目","/")
  if os.path.exists(project_path[1]) and os.path.isdir(project_path[1]):
    s_backup=os.getcwd()
    os.chdir(project_path[1])
    if os.path.exists("base"):
      rom()
    if len(os.listdir("."))!=0:
      msg("错误","文件夹非空。")
      os.chdir(s_backup)
      continue
    while 1:
      target=fselect("打开ROM",os.getenv("HOME"))
      if target[0]!=CHOICE_OK:
        if yesno("不选择ROM","确定继续吗?大部分功能可能出错。")==CHOICE_OK:
          progress("请稍等","建立项目文件...",0)
          os.mkdir("temp")
          os.mkdir("mount")
          os.mkdir("target")
          os.mkdir("base")
          os.mkdir("conv")
          progress("请稍等","处理完成",100)
          rom()
        else:
          continue
      elif os.path.exists(target[1]) and os.path.isfile(target[1]) and target[1].endswith(".zip"):
        progress("请稍等","建立项目文件...",0)
        os.mkdir("temp")
        os.mkdir("mount")
        os.mkdir("target")
        os.mkdir("conv")
        progress("请稍等","解压ROM文件...",50)
        os.mkdir("base")
        os.system("unzip -qq -d base \""+target[1].replace("\"","\\\"")+"\"")
        progress("请稍等","处理完成",100)
        rom()
      else:
        msg("错误","ROM包错误。")
  elif project_path[1]=='' and (project_path[0]==CHOICE_NO or project_path[0]==CHOICE_EXIT):
    exitmenu()
  else:
    msg("错误","无法访问这个文件夹。")