set number
set viminfo='100,<100,s10,h 
"set hlsearch

"to start the vi in insert mode Ecs key is preserved ! 
:startinsert

"blocks comment 
"select with SHIFT+v and than hit # (for uncomment -#)
vnoremap # :s#^#\##<cr>
vnoremap -# :s#^\###<cr>

"block indent 
" also use SHIFT+v to select and that SHIFT + > (or <) 

"leave "+ regitry available for the system after closing vi
autocmd VimLeave * call system("xsel -ib", getreg('+'))
"requires xsel 

set mouse=a 
