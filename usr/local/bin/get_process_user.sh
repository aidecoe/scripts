#!/bin/bash

trim() {
    local var=$@
    var="${var#"${var%%[![:space:]]*}"}"   # remove leading whitespace characters
    var="${var%"${var##*[![:space:]]}"}"   # remove trailing whitespace characters
    echo -n "$var"
}

process_name="$1"
[[ $process_name ]] || exit 1
pid="$(pgrep -n "$process_name")"
[[ $pid ]] || exit 2
uid_pid="$(ps -e -ouid -opid | egrep " $pid\$")"
uid="${uid_pid%$pid}"
uid=$(trim "$uid")
[[ $uid ]] || exit 3
passwd_line="$(getent passwd $uid)"
user_name="${passwd_line%%:*}"
[[ $user_name ]] || exit 4

echo "$user_name"
