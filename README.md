# Secret Santa
A Pyhton script that automates the extraction for names for secret santa.
## Usage
```bash
$ python3 secretsanta.py credentials.json names.csv blacklist.csv
```
### What are those files
- credentials.json
    A file with your email SMTP credentials to send emails with. It's formatted as follows:
    ```json
    {
        "server": "smtp_server_url (example: smtp.gmail.com)"
        "email": "your@email.here",
        "password": "yourPasswordOrToken"
    }
    ```
- names.csv
    A csv file structured as follows
    ```csv
    email1;name1
    email..;name..
    emailN;nameN
    ```
- blacklist.csv
    A file of email couples that will not be matched.


