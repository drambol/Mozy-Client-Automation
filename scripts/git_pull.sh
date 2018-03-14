#!/bin/bash

git rev-parse --is-inside-work-tree
git config remote.origin.url ssh://gerrit.dechocorp.com:29418/ClientQAAutomation
sudo -u jenkins git -c core.askpass=true fetch --tags --progress ssh://gerrit.dechocorp.com:29418/ClientQAAutomation +refs/heads/*:refs/remotes/origin/*
commit=`git rev-parse refs/remotes/origin/master^{commit}`
git checkout -b $commit
git rev-list $commit