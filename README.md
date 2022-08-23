# Crystalline Entity
Helper bot for the Star Trek Gifs Discord.

## Requirements

* Python 3.7
  * (see requirements.txt for module specific requirements)
* Write access to this folder (image archive is written out as a `json` file)

I run this with Ubuntu and/or Raspbian, but really any environment where you can just let a Python script run forever (in a `screen`/`tmux` session) is adequate.  Future plans involve turning this into a service.

## Execution

1. Install the requirements:

`python3 -m pip install -r requirements.txt`

2. Fill out the `.env` file:

Set the appropriate environment variables:

  * `TREK_TOKEN` -> your Discord bot token
  
  * `IMG_DB` -> the filename of your image database (in `json` format)
  
  * `IMG_DB_BAK` -> the filename of your image database backup (i.e., what it is copied over to)

3. Create a `tmux` session to run in background (use whatever method you fancy here):

`tmux`

4. Run the program

`python3 crystalline-entity.py`

5. Disengage

`Ctrl+B d`

## Commands

The commands as specified are fairly rigid at present.  Feel free to make them prettier if you so choose.

### Add an image (requires Starfleet Command role)

`.acr "!reaction" https://path.to.image.gif`

The expectation is that it starts with `.acr`, is followed by a double-quote enclosed trigger (with exclamation point), and followed by a link to a gif that either ends with `.gif`, `.gifv`, or contains `gfycat` within (as they have no direct link).

### Scan `#bot-commands` for content (requires Starfleet Command role)

`!scanchannel`

Because the prior bot left us, this command will scan the `#bot-commands` channel for any instance of the `.acr` command and attempt to re-build the library.  At present, its limit is set to scan 5000 messages, though it is alterable if necessary.

### Return a random gif

`!gifme`

Returns a random gif from the archive with the associated trigger (in case if you want to re-use it).

### List available gifs

`!list`

TBD

### Delete a gif (requires Starfleet Command role)

TBD

### Help menu

`!help`

TBD

### Service

To run as a service, use the included .service file and follow these comprehensive instructions (I used a Pi - should work with any `systemd` setup): https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267
  * Note: the service runs as the super user by default, so the Python packages will need to be installed as super user as well.

## Future Plans

* More intelligent image archiving (rotating, etc.)
* Updates for the invevitable April 2022 change
* Automated startup service scripts

