
git rev-parse --is-inside-work-tree
git config remote.origin.url ssh://gerrit.dechocorp.com:29418/ClientQAAutomation
git -c core.askpass=true fetch --tags --progress ssh://gerrit.dechocorp.com:29418/ClientQAAutomation +refs/heads/*:refs/remotes/origin/*
git rev-parse refs/remotes/origin/master > a.txt
set /p commit=<a.txt
echo %commit%
git checkout -b %commit%
git rev-list %commit%
del a.txt