# HonestBear
A discord bot

## Starting bot
ssh into server
```
./bot.py &
disown %1
exit
```

## Killing bot
ssh into server
```
ps -ef | grep bot.py
```
find (PID)
```
kill -15 (PID)
exit
```
