#!/bin/sh

lazy_start() {
    until pgrep "${WM##*/}" >/dev/null; do
        sleep 1
    done
    sleep 1
    conkymgr start
}

start() {
    lazy_start &
}

stop() {
    conkymgr stop
}
