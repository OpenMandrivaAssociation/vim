if ( -x /bin/id ) then
    if ( "`/bin/id -u`" > 200 ) then
        alias vi vim
    endif
endif

