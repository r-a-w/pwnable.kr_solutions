#set follow-fork-mode parent
#set detach-on-fork off
#handle SIGSEGV nostop
#handle SIGSEGV noprint
#handle SIGSEGV nopass
handle SIGALRM nostop
#handle SIGKILL nostop
##set pagination off
##set non-stop on
#set schedule-multiple on
##set scheduler-locking off
##b main
#b *0x000055555555500d
#set breakpoint pending on
#b *main+226
#disable 1
#set $heap=0x555555757000
#r newexploit.py
##r exploit.py
##set watch *0x0000555555555258 == "read"


#set follow-fork-mode child
#b main
##b /home/raw/Documents/pwnable/grotesque/lokihardt/lokihardt:*0x00005555555551a5
##disable 2
#set $heap=0x555555757000
#r exploit.py


