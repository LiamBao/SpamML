ps ax|grep "python spammer.py"|grep -v grep|awk '{print $1}'|xargs kill
