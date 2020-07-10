# Usage:
1. get sendgrid api key for sending emails
2. verify from email address in sendgrid
3. install requirements
4. tested on python3
```sh
export FROMEMAIL='xxxxx@xxxxxxx.com'
export SENDGRID_API_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
python positka.py --ip 3.86.128.32 --username admin --password xxxxx --email xxxx@xxxxx.com --query 'index="_internal" | head 1000' --earliest_time '2020-07-01 12:03:30' --latest_time '2020-07-10 12:03:30'
```
