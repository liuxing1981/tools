#########################################################################
# File Name: install.sh
# Author: xliu074
# mail: xing.1.liu@nokia-sbell.com
# Created Time: 2019-11-07 15:12
#########################################################################
#!/bin/bash
cp vimrc ~/.vimrc
cp validate_json.py ~/bin/
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
