#!/bin/bash
os_error_callback()
{
        #echo "in_call_back: $*"
        i=0
        while true; do
                caller $((i++)) || break
        done
        exit
        echo
}
 
trap os_error_callback ERR

