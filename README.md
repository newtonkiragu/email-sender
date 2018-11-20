# EMAIL SENDER

## Setup 

- Enable less secure from google
- Its also important to note that adding `NODE_TLS_REJECT_UNAUTHORIZED` to `false` may leave you vulnearable to MITM attacks, if you find a better solution for gmail please make a pull request. 

### Env file
- add the following to a `.env` file at the root of the dir
```bash
EMAIL_USER=EMAIL_USER
EMAIL_PASSWORD=EMAIL_PASSWORD
```
