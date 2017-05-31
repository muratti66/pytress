# Pytress

Pytress is a smtp stress tool, designed to test your email server for stress.
This software can be send e-mail in 2 ways :

  - With "Eml" files
  - With body and attachment combinations

Features :
  - Works in Background
  - Uses as many workers
  - Results and outputs write to log
  - More than one sender, recipient, subject combination
  - Body + attachment or direct mail with .eml file
  - Shows the smtp processing time

# Installation :
Clone git project to server
```sh
git clone (URL)
```
Install the dependencies

```sh
$ cd pytress
$ pip install -r requirements.pip
```

Choosing the method of use and preparation :

```sh
ln -s config_withattach.ini config.ini
ln -s thread_withattach.py thread.py
```
-- or --
```sh
ln -s config_withbody.ini config.ini
ln -s thread_withbody.py thread.py
```
Config file edit:
```sh
vi config.ini
```
```vim
[SERVER]
host : x.y.z.t # set the mail server ip
port : 25 # port
timeout : 30 # smtp connection timeout value
[SENDING]
thread : 1 # How many workers will work ?
amount : 5 # How many times each worker will email send ?
[PATHS]
body : bodys # email bodys folder path
attachment : attachments  # email attachments folder path
emlfile : emlfiles # email .eml files folder path
log : output.log # output.log path
[FROM] # How many sender email address
1 : testuser@testdomain.com
2 : testuser2@testdomain.com
[TO] # How many recipient email address
1 : testuser@testdomain.com
2 : testuser2@testdomain.com
[SUBJECTS] # how many subject use
1 : Test Subject
2 : Test Subject 2
3 : Test Subject 3
```

# Usage :

And start pytress and watch the status in log file:
```sh
~/pytress$ python ./start.py
5 emails sent to host : x.y.z.t
~/pytress$ #
~/pytress$ tail -f output.log
2017-05-31 10:30:17,758; Thread : 1; Process : 1 (2512); Status : 553; ExecTime : 0.0850939750671 (second); Detail : sorry, that domain isnt in my list of managed domains (#5.7.1)
2017-05-31 10:30:17,835; Thread : 1; Process : 2 (2512); Status : 553; ExecTime : 0.0736820697784 (second); Detail : sorry, that domain isnt in my list of managed domains (#5.7.1)
2017-05-31 10:30:17,918; Thread : 1; Process : 3 (2512); Status : 553; ExecTime : 0.0779161453247 (second); Detail : sorry, that domain isnt in my list of managed domains (#5.7.1)
2017-05-31 10:30:17,992; Thread : 1; Process : 4 (2512); Status : 553; ExecTime : 0.0698771476746 (second); Detail : sorry, that domain isnt in my list of managed domains (#5.7.1)
2017-05-31 10:30:18,071; Thread : 1; Process : 5 (2512); Status : 553; ExecTime : 0.0749490261078 (second); Detail : sorry, that domain isnt in my list of managed domains (#5.7.1)
```


License
----

GNU
