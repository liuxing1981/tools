F1  tree for view
F3  clear search result
F4  close all files = wqa
F5  run the script
F6  change to another window
F12 remove empty line and spaces at the end of line

ctrl+a select all
ctrl+d comment line
ctrl+n next file
ctrl+p previous file
,f validate and format json
,r run current line with bash shell
," add " surround a word
,ev open .vimrc file
,sv reload .vimrc file


note: 
Type "#args: a b c" in your script could pass the args the script needs.
for ex:
#!/bin/bash
#args: /tmp
ls $1

If the args is /tmp the command is ls /tmp. This is only used for test when press F5 to run.

Install vbunlde to manage vim plugin
cp *.ttf /usr/share/fonts 在服务器端，如果有必要
在客户端的terminal也要导入这个字体

