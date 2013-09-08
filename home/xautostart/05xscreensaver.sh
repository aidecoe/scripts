#!/bin/sh

start() {
    xscreensaver &
}

stop() {
    killall xscreensaver
}
