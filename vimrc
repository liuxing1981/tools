let s:author=substitute(system("whoami"),'\%x00',"","g")
let s:mail=substitute(system('str=$(cat ~/.gitconfig|grep "email =");str=${str##*=};echo $str'),'\%x00',"","g")
if has("syntax")
	syntax on            " 语法高亮
endif
colorscheme ron        " elflord ron peachpuff default 设置配色方案，vim自带的配色方案保存在/usr/share/vim/vim72/colors目录下
" detect file type
filetype on
filetype plugin on
" If using a dark background within the editing area and syntax highlighting
" turn on this option as well
set background=dark
" Uncomment the following to have Vim jump to the last position when
" reopening a file
if has("autocmd")
	au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
	"have Vim load indentation rules and plugins according to the detected filetype
	filetype plugin indent on
endif
" The following are commented out as they cause vim to behave a lot
" differently from regular Vi. They are highly recommended though.
"set ignorecase        " 搜索模式里忽略大小写
"set smartcase        " 如果搜索模式包含大写字符，不使用 'ignorecase' 选项。只有在输入搜索模式并且打开 'ignorecase' 选项时才会使用。
set autowrite        " 自动把内容写回文件: 如果文件被修改过，在每个 :next、:rewind、:last、:first、:previous、:stop、:suspend、:tag、:!、:make、CTRL-] 和 CTRL-^命令时进行；用 :buffer、CTRL-O、CTRL-I、'{A-Z0-9} 或 `{A-Z0-9} 命令转到别的文件时亦然。
set autoindent        " 设置自动对齐(缩进)：即每行的缩进值与上一行相等；使用 noautoindent 取消设置
set smartindent        " 智能对齐方式
set tabstop=4        " 设置制表符(tab键)的宽度
set softtabstop=4     " 设置软制表符的宽度
set shiftwidth=4    " (自动) 缩进使用的4个空格
set cindent            " 使用 C/C++ 语言的自动缩进方式
set cinoptions={0,1s,t0,n-2,p2s,(03s,=.5s,>1s,=1s,:1s     "设置C/C++语言的具体缩进方式
"set backspace=2    " 设置退格键可用
set showmatch        " 设置匹配模式，显示匹配的括号
set linebreak        " 整词换行
set whichwrap=b,s,<,>,[,] " 光标从行首和行末时可以跳到另一行去
"set hidden " Hide buffers when they are abandoned
set mouse=            " Enable mouse usage (all modes)    "使用鼠标
set number            " Enable line number    "显示行号
"set previewwindow    " 标识预览窗口
set history=50        " set command history to 50    "历史记录50条
"--状态行设置--
set laststatus=2 " 总显示最后一个窗口的状态行；设为1则窗口数多于一个的时候显示最后一个窗口的状态行；0不显示最后一个窗口的状态行
set ruler            " 标尺，用于显示光标位置的行号和列号，逗号分隔。每个窗口都有自己的标尺。如果窗口有状态行，标尺在那里显示。否则，它显示在屏幕的最后一行上。
"--命令行设置--
set showcmd            " 命令行显示输入的命令
set showmode        " 命令行显示vim当前模式
"--find setting--
set incsearch        " 输入字符串就显示匹配点
set hlsearch

" defined by luis
let mapleader=","
set autoread
noremap <C-a> ggVG<CR>
"delete space at end of line
noremap <silent> <F1> i<CR><ESC>
"clear hightlight search words
noremap <silent> <F3> :let @/=""<CR>
noremap <silent> <F4> :wqa<CR>
noremap <silent> <leader>w :wqa<CR>
inoremap <silent> <F4> <ESC>:wqa<CR>
noremap <silent> <F5> :call Run()<CR><CR>
inoremap <silent> <F5> <ESC>:call Run()<CR><CR>
nnoremap <silent> <F6> <C-w>w<CR>
"auto indent
nnoremap <silent> <F8> gg=G
"delete empty lines
noremap <silent> <F12> :call Drop_tail()<CR>
noremap <silent> f gg=G
noremap <silent> <leader>f gg=G
noremap <silent> <C-d> :call Comment(getline('.'))<CR>
"noremap <silent> <C-j> :call Down_text()<CR>
"noremap <silent> <C-k> :call Up_text()<CR>
inoremap <silent> <S-CR> <ESC>O
func Drop_tail()
	" delete empty lines
	exec 'g/^\s*$/d'
	" delete ^M
	exec '%s/\r//g'
	exec '%s/\%x00/ /g'
	" delete empty spaces of line
	exec '%s/ *$//'
endfunc

func Hlsearch()
endfunc

func Down_text()
	let s:last = getline('.')
	let s:pos = line('.')
	if s:pos != line('$')
		call append(s:pos+1,s:last)
		normal ddj
	endif
endfunc

func Up_text()
	let s:first = getline('.')
	let s:pos = line('.')
	if s:pos-1 != line('^')
		call append(s:pos-2,s:first)
		normal ddkk
	endif
endfunc
func Comment(line)
	if matchstr(a:line,"^#") == "#"
		:s/^#//
	else
		:s/^/#/
	endif
endfunc
autocmd BufNewFile *.pl,*.py,*.sh,*.exp exec ":call SetTitle()" 
autocmd BufNewFile * exec ":normal G" 
func SetTitle()
	call setline(1,"\#########################################################################")
	call append(line("."), "\# File Name: ".expand("%"))
	call append(line(".")+1, "\# Author: ".s:author)
	call append(line(".")+2, "\# mail: ".s:mail)
	call append(line(".")+3, "\# Created Time: ".strftime("20%y-%m-%d %H:%M"))
	call append(line(".")+4, "\#########################################################################")

	"如果文件类型为.sh文件
	if &filetype == 'sh'
		call append(line(".")+5, "\#!/bin/bash")
	elseif &filetype == 'python'
		call append(line(".")+5, "\#!/usr/bin/python")
	elseif &filetype == 'perl'
		call append(line(".")+5, "\#!/usr/bin/perl")
	elseif &filetype == 'expect'
		call append(line(".")+5, "\#!/usr/bin/expect")
	endif
	call append(line(".")+6, "")
endfunc

let s:open_flag=0
func Run()
	if &filetype == 'sh' || &filetype == 'python'|| &filetype == 'perl'|| &filetype == 'expect'
		exe "normal! mq"
		if s:open_flag == 0
			let s:open_flag=1
			call Run_script()
			execute "rightbelow vsplit %.out"
		else
			call Run_script()
		endif
		exe "normal! \<C-W>\<C-h>`q"
	endif
endfunc

let s:args =""
func GetArgs()
	for n in getline(1,30)
		if n =~ '^#args:'
			let s:args = substitute(n,'^#args: ',"","")
			break
		endif
	endfor
endfunc

func Run_script()
	call GetArgs()
	:w!
	if &filetype == 'sh'
		execute ':!clear && sh % ' . s:args . ' 2>&1 | tee %.out'
	elseif &filetype == 'python'
		execute ':!clear && python % ' . s:args . ' 2>&1 | tee %.out'
	elseif &filetype == 'perl'
		execute ':!clear && perl % ' . s:args . ' 2>&1 | tee %.out'
	elseif &filetype == 'expect'
		execute ':!clear && expect % ' . s:args . ' 2>&1 | tee %.out'
	endif
endfunc
"hi String ctermfg = darkred
