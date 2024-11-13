# Secret Santa
A web service to create secret santa automatically.
> [!Note]
> This project is currently being updated, so it's broken.

## Usage
Build and run the docker compose service:
```bash
$ docker compose up --build
```
The container exposes on the port `9090` the web service.

### Create a store
People are stored inside the `santastores` directory and are JSON files named with the ID of the store. After creating one
with the following base structure:
```json
{
  "name": "Test Store",
  "people": [],
  "deny_pairs": [],
  "end_date": "ISO Format Time"
}
```
You can access it by adding `?store_id=filename-without-the-.json` to the url.

### Set up email sending
Create a `.env` file and copy the template present inside the `.env.sample` template. Fill it in with your credentials 
and start the server up.

## Features
Features that are not ticked still have to be added
- [x]: User registration
- []: Automatic sending of emails inside the store when the end time has been reached
- []: Online store creation
- []: Block list of email address pairs that won't be matched

## License
This software is licensed under the [GNU GPLv3 License](COPYING) and provides no warranties in any way. I am not responsible 
for anything that the end user (you) does. I am not responsible in any way for any privacy violation that can happen during 
the usage of this software. The software (SecretSanta) is provided AS IS. Any issues encountered can be reported by opening 
a GitHub Issue, but they might be ignored and not fixed.

## Dependencies and other libraries
- Uses `fastapi` and `uvicorn` for the web service
- Uses `bootstrap` for the web UI
- Used `bootstrapemail.com` to create the HTML files for the emails
