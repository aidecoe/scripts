#!/bin/bash

# Requires:
# - get_process_user.sh (which can be found in this repository)
# - xscreensaver
# - pm-utils

LOGP="LID closed"

lock_screen() {
    local user="$(/usr/local/bin/get_process_user.sh xscreensaver)"
    local lock="/usr/bin/xscreensaver-command -lock"

    if [[ ! $user ]]; then
        logger -p auth.warning "$LOGP: xscreensaver is not running"
        return 1
    fi

    if su "$user" -c "$lock" ; then
        logger -p auth.info "$LOGP: successfully locked screen for user $user"
        return 0
    else
        logger -p auth.err "$LOGP: locking screen failed!"
        return 1
    fi
}

is_on_battery() {
    local online="$(</sys/class/power_supply/ACAD/online)"
    [[ $online = 0 ]]
}

pm_suspend() {
    if ! /usr/sbin/pm-suspend; then
        logger -p user.err "$LOGP: pm-suspend failed!"
        return 1
    fi
}

on_close() {
    if lock_screen; then
        if is_on_battery; then
            logger -p user.info "$LOGP: laptop on battery - suspending..."
            pm_suspend
        else
            logger -p user.info "$LOGP: laptop on AC - keeping active"
        fi
    fi
}

if [[ $2 = LID ]]; then
    case "$3" in
        close) on_close ;;
    esac
fi
