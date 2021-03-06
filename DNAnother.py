#!/usr/bin/env python3
#coding=utf-8
#copyright (c) 2021 awathefox.
#This program was under the LGPLv2.1 license.
import os
import subprocess
import sys
import shutil
import json
import traceback
#dialog begin
def choice(run,default=""): # run=['title','menu',['title','obj'],['title','obj'],...]
  cmd="dialog --title "+json.dumps(run[0],ensure_ascii=False)+" --default-item "+json.dumps(default,ensure_ascii=False)+" --menu "+json.dumps(run[1],ensure_ascii=False)+" 0 0 0 "
  s=2
  while s < len(run):
    cmd+=json.dumps(run[s][0],ensure_ascii=False)+" "+json.dumps(run[s][1],ensure_ascii=False)+" "
    s=s+1
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def inputbox(title,msg,default=""):
  cmd="dialog --title "+json.dumps(title,ensure_ascii=False)+" --inputbox "+json.dumps(msg,ensure_ascii=False)+" 0 0 "+json.dumps(default,ensure_ascii=False)
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def textbox(title,file):
  cmd="dialog --title "+json.dumps(title,ensure_ascii=False)+" --textbox "+json.dumps(file,ensure_ascii=False)+" 0 0"
  os.system(cmd)
  return
def fselect(title,dir=""):
  cmd="dialog --title "+json.dumps(title,ensure_ascii=False)+" --fselect "+json.dumps(dir,ensure_ascii=False)+" 20 50"
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def dselect(title,dir=""):
  cmd="dialog --title "+json.dumps(title,ensure_ascii=False)+" --dselect "+json.dumps(dir,ensure_ascii=False)+" 20 50"
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode()]
def mulchoice(run): #run=['title','menu',['title','obj'],['title','obj'],...]
  cmd="dialog --title "+json.dumps(run[0],ensure_ascii=False)+" --checklist "+json.dumps(run[1],ensure_ascii=False)+" 0 0 "+str(len(run[2:]) if len(run[2:]) < 5 else 5)+" "
  s=2
  while s < len(run):
    cmd+=json.dumps(run[s][0],ensure_ascii=False)+" "+json.dumps(run[s][1],ensure_ascii=False)+" "+str(s-1)+" "
    s=s+1
  x=subprocess.run(cmd,stderr=subprocess.PIPE,shell=True)
  return [x.returncode,x.stderr.decode().split(' ')]
def msg(title,msg):
  cmd="dialog --title "+json.dumps(title,ensure_ascii=False)+" --msgbox "+json.dumps(msg,ensure_ascii=False)+" 0 0"
  os.system(cmd)
  return
def infobox(title,msg):
  cmd="dialog --title "+json.dumps(title,ensure_ascii=False)+" --infobox "+json.dumps(msg,ensure_ascii=False)+" 20 50"
  os.system(cmd)
  return
def progress(title,msg,percent):
  cmd="echo "+str(percent)+" | dialog --title "+json.dumps(title,ensure_ascii=False)+" --gauge "+json.dumps(msg,ensure_ascii=False)+" 20 50 "+str(percent)
  os.system(cmd)
  return
def yesno(title,msg,yesbutton="???",nobutton="???"):
  cmd="dialog --title "+json.dumps(title,ensure_ascii=False)+" --yes-label "+json.dumps(yesbutton,ensure_ascii=False)+" --no-label "+json.dumps(nobutton,ensure_ascii=False)+" --yesno "+json.dumps(msg,ensure_ascii=False)+" 0 0"
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
def dat2img(list,source,output,sparse=False):
  if sparse:
    os.system("python3 {0}/bin/sdat2img/sdat2img.py {1} {2} temp/output.tmp.img >/dev/null".format(sys.path[0],list,source))
    os.system("img2simg temp/output.tmp.img {0}".format(output))
    os.remove("temp/output.tmp.img")
  else:
    os.system("python3 {0}/bin/sdat2img/sdat2img.py {1} {2} {3} >/dev/null".format(sys.path[0],list,source,output))
def img2dat(source,output,prefix):
  if gettype(source).startswith("Android sparse image"):
    os.system("python3 {0}/bin/img2sdat/img2sdat.py -v 4 {1} -p {2} -o {3} >/dev/null".format(sys.path[0],source,prefix,output))
  else:
    os.system("python3 {0}/bin/rimg2sdat/rimg2sdat.py -v 4 {1} -p {2} -o {3} >/dev/null".format(sys.path[0],source,prefix,output))
#dat<->img end

#img<->dir begin
def createFile(name,size,bs=1024*1024*500): #bs is set to 500MiB
  with open(name,"wb") as f:
    while size>bs:
      f.write(b'\0'*bs)
      size-=bs
    f.write(b'\0'*size)
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
    os.system("mv -f temp/abootimg/. "+output)
  else:
    if gettype(source).startswith("Android sparse image"):
      os.system("simg2img {0} temp/output.tmp.img > /dev/null")
      source="temp/output.tmp.img"
    os.system("mount -o ro {0} mount".format(source))
    os.system("cp -r mount/. {0}".format(output))
    os.system("umount mount")
    if source=="temp/output.tmp.img":
      os.remove(source)
  return os.path.getsize(source)
def packimg(source,output,size,sparseimg=False):
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
  else:
    createFile("temp/output.tmp.img",size)
    os.system("mkfs.ext2 -L "+source.split("/")[-1]+" -O large_file,huge_file,extent -d {0} temp/output.tmp.img > /dev/null".format(source))
    if sparseimg:
      os.system("img2simg temp/output.tmp.img {0}".format(output))
      os.remove("temp/output.tmp.img")
    else:
      shutil.move("temp/output.tmp.img",output)
  return os.path.getsize(output) #??????sparse_img???size ????????????
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
    os.system("python3 {0}/bin/payload_dumper/payload_dumper.py {1} --out {2} > /dev/null".format(sys.path[0],payload,output))
  else:
    os.system("python3 {0}/bin/payload_dumper/payload_dumper.py {1} --out {2} --images {3} > /dev/null".format(sys.path[0],payload,output,",".join(images)))
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
        s=fselect("?????? "+path.split("/")[-1].split(".")[0]+".transfer.list")
      else:
        s=[CHOICE_OK,'conv/output.transfer.list']
      if s[0]!=CHOICE_OK:
        if yesno("????????????","?????????????????????????")==CHOICE_OK:
          clearconv()
          return ''
      elif os.path.exists(s[1]) and os.path.isfile(s[1]) and s[1].endswith(".list"):
        infobox("????????????","??????????????????,?????????...")
        dat2img(s[1],path,'conv/output.img',True)
        if path.startswith('conv/'):
          shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
        return 'conv/output.img'
      else:
        msg("????????????","?????????????????????")
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
    while 1:
      s=inputbox("????????????","????????????????????????????????????\n???????????????size.json?????????????????????img????????????")
      if s[0]!=CHOICE_OK:
        if yesno("????????????","?????????????????????????")==CHOICE_OK:
          clearconv()
          return ''
      elif s[1].isdigit() and int(s[1])>=0:
        infobox("????????????","??????????????????,?????????...")
        packimg(path,'conv/output.img',int(s[1]),True)
        if path.startswith('conv/'):
          shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
        return 'conv/output.img'
      else:
        msg("????????????","??????????????????")
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
  infobox("?????????","???????????????")
  cleartemp()
  if yesno("????????????","?????????????????????????????????????????????\n??????????????????????")==CHOICE_OK:
    infobox("?????????","???????????? conv")
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
    x=inputbox("????????????","??????????????????????????????????????????????????????\n???????????????:br,dat,img,dir,bin\n??????:?????????->????????????")
    if x[0]!=CHOICE_OK:
      return None
    else:
      a=x[1].split("->")
      if len(a)<2 or conv[a[0]]==None or conv[a[0]][a[1]]==None:
        msg("????????????","???/????????????????????????????????????")
      q=fselect("???????????????")
      if q[0]!=CHOICE_OK:
        return None
      elif os.path.exists(q[1]) and (q[1].endswith("."+a[0]) or (os.path.isdir(q[1]) and a[0]=="dir")):
        path=q[1]
        for x in range(len(conv[a[0]][a[1]])):
          progress("????????????","???????????? "+conv[a[0]][a[1]][x]+" ["+str(x)+"/"+str(len(conv[a[0]][a[1]]))+"]",round((x/len(conv[a[0]][a[1]]))*100))
          path=convert(path,conv[a[0]][a[1]][x])
          if path=="":
            msg("????????????","???????????????")
            break
        if path=="":
          return None
        else:
          msg("????????????","?????????\n?????????????????? "+path+"???")
      else:
        msg("????????????","??????(???)???????????????")
        return None
def rom():
  global bro_ext_arg
  global zip_ext_arg
  if os.path.exists("base") and os.path.isdir("base"):
    while 1:
      ch=choice([
        "DNAnother v1.0.3-stable",
        "?????????????????????????????????????????????",
        ["1","??????"],
        ["2","??????"],
        ["3","??????"],
        ["4","??????"],
        ["5","??????"],
        ["6","??????"],
      ])[1]
      if ch=='' or ch=='6':
        exitmenu()
      elif ch=='1':
        f=[
          '??????',
          '???????????????????????????',
        ]
        infobox("DNAnother","??????????????????")
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
          msg("DNAnother","????????????????????????????????????")
          continue
        x=mulchoice(f)
        infobox("DNAnother","???????????????")
        cleartemp()
        if x[0]==CHOICE_OK and x[1]!=['']:
          x=x[1]
          fail=False
          progress("DNAnother","???????????????",0)
          if os.path.exists("target/size.json") and os.path.isfile("target/size.json"):
            with open("target/size.json") as f:
              sizetable=json.loads(f.read())
          else:
            sizetable={}
          for i in x:
            z=os.path.splitext(i)
            if os.path.exists("target/{0}".format(i.split(".")[0])):
              if yesno(i,"????????????????????????????????????????????????\n??????????????????????????????")!=CHOICE_OK:
                progress(i,"???????????????",100)
                continue
              else:
                progress(i,"??????????????????...",0)
                shutil.rmtree("target/{i}".format(i.split(".")[0]),True)
            if z[1]==".br":
              progress(i,"???????????? br2dat [1/3]",round(1/6*100))
              br2dat("base/{0}".format(i),"temp/{0}.tmp.dat".format(i))
              progress(i,"???????????? dat2img [2/3]",round(2/6*100))
              while 1:
                if not os.path.exists("base/{0}.transfer.list".format(i.split(".")[0])):
                  s=fselect("?????? "+i.split(".")[0]+".transfer.list")
                else:
                  s=[CHOICE_OK,'base/{0}.transfer.list'.format(i.split(".")[0])]
                if s[0]!=CHOICE_OK:
                  if yesno(i,"?????????????????????????")==CHOICE_OK:
                    cleartemp()
                    fail=True
                    break
                elif os.path.exists(s[1]) and os.path.isfile(s[1]) and s[1].endswith(".list"):
                  infobox(i,"??????????????????,?????????...")
                  dat2img(s[1],"temp/{0}.tmp.dat".format(i),"temp/{0}.tmp.img".format(i))
                  break
                else:
                  msg(i,"?????????????????????")
              progress(i,"???????????? dat2img [2/3]",round(3/6*100))
              os.remove("temp/{0}.tmp.dat".format(i))
              progress(i,"???????????? unpackimg [3/3]".format(i),round(4/6*100))
              sizetable[i.split(".")[0]]=[]
              sizetable[i.split(".")[0]].append(unpackimg("temp/{0}.tmp.img".format(i),"target/{0}".format(i.split(".")[0])))
              sizetable[i.split(".")[0]].append(gettype("temp/{0}.tmp.img".format(i)).split(",")[1][6:])
              progress(i,"???????????? unpackimg [3/3]",round(5/6*100))
              os.remove("temp/{0}.tmp.img".format(i))
              progress(i,"????????????",100)
            elif z[1]==".dat":
              progress(i,"???????????? dat2img [1/2]",round(1/4*100))
              while 1:
                if not os.path.exists("base/{0}.transfer.list".format(i.split(".")[0])):
                  s=fselect("?????? "+i.split(".")[0]+".transfer.list")
                else:
                  s=[CHOICE_OK,'base/{0}.transfer.list'.format(i.split(".")[0])]
                if s[0]!=CHOICE_OK:
                  if yesno(i,"?????????????????????????")==CHOICE_OK:
                    cleartemp()
                    fail=True
                    break
                elif os.path.exists(s[1]) and os.path.isfile(s[1]) and s[1].endswith(".list"):
                  infobox(i,"??????????????????,?????????...")
                  dat2img(s[1],"base/{0}".format(i),"temp/{0}.tmp.img".format(i))
                else:
                  msg(i,"?????????????????????")
              progress(i,"???????????? unpackimg [2/2]".format(i),round(2/4*100))
              sizetable[i.split(".")[0]]=unpackimg("temp/{0}.tmp.img".format(i),"target/{0}".format(i.split(".")[0]))
              progress(i,"???????????? unpackimg [2/2]",round(3/4*100))
              os.remove("temp/{0}.tmp.img".format(i))
              progress(i,"????????????",100)
            elif z[1]==".img":
              progress(i,"???????????? unpackimg [1/1]".format(i),round(1/2*100))
              sizetable[i.split(".")[0]]=unpackimg("base/{0}".format(i),"target/{0}".format(i.split(".")[0]))
              progress(i,"????????????",100)
            elif z[1]==".bin":
              if yesno("?????? - "+i,"???????????????payload.bin??????\n?????????????????????????????????????????????")!=CHOICE_OK:
                continue
              if yesno("?????? - "+i,"???????????????payload.bin?????????????????????????????????????????????????????????\n??????????????????????????????")!=CHOICE_OK:
                continue
              infobox(i,"???????????? target")
              cleartarget()
              infobox(i,"????????????????????????")
              sizetable={}
              infobox(i,"??????")
              infobox(i,"??????????????????...")
              a=payload_partitions("base/"+i)
              p=[
                i,
                "???????????????????????????",
              ]
              for d in range(len(a)):
                p.append([str(d+1),a[d]])
              p=mulchoice(p)
              if p[0]==CHOICE_OK:
                p=p[1]
                infobox(i,"??????????????????...")
                fin=[]
                for l in p:
                  fin.append(a[int(l)-1])
                progress(i,"???????????? extract_payload [1/1]",100)
                extract_payload("base/"+i,"temp/",fin)
                for g in os.listdir("temp/"):
                  c=gettype("temp/"+g)
                  if c.startswith("Android sparse image") or c.startswith("Android bootimg") or c.startswith("Linux rev 1.0 ext2 filesystem data"):
                    progress(i+"->"+g,"???????????? unpackimg [1/1]",50)
                    sizetable[i.split(".")[0]]=unpackimg("temp/{0}".format(g),"target/{0}".format(g.split(".")[0]))
                    progress(i+"->"+g,"???????????? unpackimg [1/1]",100)
                    os.remove("temp/{0}".format(g))
                    progress(i+"->"+g,"????????????",100)
                  else:
                    progress(i+"->"+g,"???????????? cp [1/1]",50)
                    shutil.copy("temp/{0}".format(g),"target/")
                    progress(i+"->"+g,"???????????? cp [1/1]",100)
                    os.remove("temp/{0}".format(g))
                    progress(i+"->"+g,"????????????",100)
            else:
              fail=True
              break
          with open("target/size.json","w") as f:
            f.write(json.dumps(sizetable))
          if fail:
            msg("DNAnother","???????????????\n?????????????????????????????????")
          else:
            msg("DNAnother","?????????")
      elif ch=='2':
        infobox("DNAnother","???????????????")
        cleartemp()
        file=fselect("???????????????[.zip]","/")
        progress("?????????","?????????...",0)
        if file[0]==CHOICE_OK and os.path.exists(file[1]) and os.path.isfile(file[1]) and file[1].endswith(".zip"):
          progress("?????????","?????????????????????...",0)
          os.system("unzip -d temp \""+file[1].replace("\"","\\\"")+"\"")
          progress("?????????","??????????????????...",50)
          s_backup=os.getcwd()
          os.chdir("target")
          os.system("bash ../temp/install.sh")
          os.chdir(s_backup)
          progress("?????????","????????????????????????")
          cleartemp()
          msg("????????????","?????????")
          input()
        elif file[0]==CHOICE_OK:
          msg("??????","??????????????????")
      elif ch=='3':
        if yesno("??????","?????????????????????\n??????????????????5??????????????????")==CHOICE_OK:
          infobox("DNAnother","???????????????")
          cleartemp()
          progress("DNAnother","?????????",0)
          if os.path.exists("target/size.json") and os.path.isfile("target/size.json"):
            with open("target/size.json") as f:
              sizetable=json.dumps(f.read())
          else:
            sizetable={}
          for i in os.listdir("target"):
            progress(i,"??????????????????".format(i),0)
            if os.path.isfile("target/"+i):
              progress(i,"???????????? cp [1/1]",100)
              os.system("cp target/"+i+" temp/")
            elif os.path.exists("target/"+i+"/bootimg.cfg"):
              progress(i,"???????????? packimg [1/1]".format(i),100)
              packimg("target/{0}".format(i),"temp/{0}.img".format(i),0)
              progress(i,"??????".format(i),100)
            else:
              progress(i,"???????????? packimg [1/3]".format(i),round(1/6*100))
              if type(sizetable[i])!=list or len(sizetable[i])!=2 or type(sizetable[i][0])!=int or sizetable[i][0]<0 or type(sizetable[i][1])!=str or len(sizetable[i][1])!=32:
                while 1:
                  s=inputbox(i,"?????????????????????\n??????????????????????????????")
                  if s[0]!=CHOICE_OK:
                    if yesno(i,"?????????????????????????????????")==CHOICE_OK:
                      cleartemp()
                      fail=True
                  elif s[1].isdigit() and int(s[1])>=0:
                    infobox(i,"??????????????????...")
                    packimg("target/{0}".format(i),"temp/{0}.img".format(i),int(s[1]),True)
                  else:
                    msg("??????????????????")
              else:
                packimg("target/{0}".format(i),"temp/{0}.img".format(i),sizetable[i],True)
              progress(i,"???????????? img2dat [2/3]".format(i),round(2/6*100))
              img2dat("temp/{0}.img".format(i),"temp",i)
              progress(i,"???????????? img2dat [2/3]".format(i),round(3/6*100))
              os.remove("temp/{0}.img".format(i))
              progress(i,"???????????? dat2br [3/3]".format(i),round(4/6*100))
              dat2br("temp/{0}.new.dat".format(i),"temp/{0}.new.dat.br".format(i),bro_ext_arg)
              progress(i,"???????????? dat2br [3/3]".format(i),round(5/6*100))
              os.remove("temp/{0}.new.dat".format(i))
              progress(i,"??????".format(i),100)
          progress("DNAnother","?????????",0)
          progress("DNAnother","????????????...",50)
          os.system("cp -rn base/* temp")
          progress("DNAnother","????????????...",50)
          progress("DNAnother","?????????",0)
          progress("DNAnother","?????????",0)
          os.chdir("temp")
          os.system("zip ../update.zip -rq * "+zip_ext_arg)
          os.chdir("..")
          progress("DNAnother","????????????",100)
          infobox("DNAnother","????????????????????????...")
          cleartemp()
          msg("DNAnother","?????????????????? update.zip???\n???????????????????????????")
      elif ch=='4':
        os.system("clear")
        s_backup=os.getcwd()
        os.chdir("target")
        print("??????????????? target ???????????????")
        print("???????????????????????????????????????????????????cd [?????????]")
        print("DNAnother ?????????????????????")
        print("??????:????????????????????????????????????")
        print("???root????????????ROM??????????????????????????????")
        os.system("bash")
        os.chdir(s_backup)
      elif ch=='5':
        while 1:
          ch=choice([
            "??????",
            "????????????????????????????????????\n????????????????????????????????????",
            ["1","?????? temp"],
            ["2","?????? target"],
            ["3","????????????"],
            ["4","??????????????????"],
            ["5","??????"],
            ["6","??????"],
          ])[1]
          if ch=='' or ch=='6':
            break
          elif ch=='1':
            infobox("?????????","???????????? temp")
            cleartemp()
          elif ch=='2':
            if yesno("??????","???????????????????????????????????????????????????????????????\n??????????????????????????????")==CHOICE_OK:
              infobox("?????????","???????????? target")
              cleartarget()
          elif ch=='3':
            highconv()
          elif ch=='4':
            ch=choice([
              "??????????????????",
              "??????????????????????????????",
              ["1","zip"],
              ["2","brotli"]
            ])
            if ch[0]==CHOICE_OK:
              if ch[1]=='1':
                x=inputbox("??????????????????","?????????zip???????????????:",zip_ext_arg)
                if x[0]==CHOICE_OK:
                  zip_ext_arg=x[1]
                  msg("??????????????????","??????????????????")
              if ch[1]=='2':
                x=inputbox("??????????????????","?????????brotli???????????????:",bro_ext_arg)
                if x[0]==CHOICE_OK:
                  bro_ext_arg=x[1]
                  msg("??????????????????","??????????????????")
          elif ch=='5':
            if not os.path.exists("{0}/about.txt".format(sys.path[0])) or not os.path.isfile("{0}/about.txt".format(sys.path[0])):
              msg("??????","????????????????????????")
            else:
              textbox("??????","{0}/about.txt".format(sys.path[0]))
  else:
    msg("??????","???????????????????????????????????????")
    exitmenu()
if os.geteuid() != 0:
  msg("??????","????????????sudo???????????????")
  exitmenu()
while 1:
  project_path=dselect("????????????","/")
  if project_path[0]!=CHOICE_OK:
    exitmenu()
  elif os.path.exists(project_path[1]) and os.path.isdir(project_path[1]):
    s_backup=os.getcwd()
    os.chdir(project_path[1])
    if os.path.exists("base"):
      rom()
    if len(os.listdir("."))!=0:
      msg("??????","??????????????????")
      os.chdir(s_backup)
      continue
    while 1:
      target=fselect("??????ROM",os.getenv("HOME"))
      if target[0]!=CHOICE_OK:
        if yesno("?????????ROM","??????????????????????????????????????????????")==CHOICE_OK:
          progress("?????????","??????????????????...",0)
          os.mkdir("temp")
          os.mkdir("mount")
          os.mkdir("target")
          os.mkdir("base")
          os.mkdir("conv")
          progress("?????????","????????????",100)
          try:
            rom()
          except Exception as f:
            if yesno("????????????","?????????????????????????????????\n\n"+traceback.format_exc()+"\n???????????????????????????????????????","??????","????????????")==CHOICE_OK:
              exitmenu()
            else:
              rom()
        else:
          continue
      elif os.path.exists(target[1]) and os.path.isfile(target[1]) and target[1].endswith(".zip"):
        progress("?????????","??????????????????...",0)
        os.mkdir("temp")
        os.mkdir("mount")
        os.mkdir("target")
        os.mkdir("conv")
        progress("?????????","??????ROM??????...",50)
        os.mkdir("base")
        os.system("unzip -qq -d base \""+target[1].replace("\"","\\\"")+"\"")
        progress("?????????","????????????",100)
        try:
          rom()
        except Exception as f:
          if yesno("????????????","?????????????????????????????????\n\n"+traceback.format_exc()+"\n???????????????????????????????????????","??????","????????????")==CHOICE_OK:
            exitmenu()
          else:
            rom()
      else:
        msg("??????","ROM????????????")
  else:
    msg("??????","??????????????????????????????")
