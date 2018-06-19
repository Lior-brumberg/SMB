@echo off
secedit /configure /db %temp%\temp.sdb /cfg mypolicy.inf
net use T: \\ido-pc\Users
pause