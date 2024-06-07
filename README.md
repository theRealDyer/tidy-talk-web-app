Some of the files/folders _not_ uploaded to remote repo, i.e., contain sensitive info and hence are part of `.gitignore`:
* `node_modules/` (would need installing on fresh local copy)
* `.env` (contains environment variables including API key)

This version uses env variables (not currently working when pushed to firebase (Env variables can probably be stored in firebase to ensure a fully working package), whereas my local copy does still have the API hard coded into `app.py`.
