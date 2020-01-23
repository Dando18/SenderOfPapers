# SenderOfPapers

I made this project to send me papers to read at regular intervals. It's not very robust and largely dependent on gmail mailboxes, but feel free to use or extend it as you'd like.

It works like so: 

`python3 main.py --send` will determine the next article to send and email it.

`python3 main.py --check` will check if any previous emails got a response and save the response if there was one.

The next file chosen to send is the first pdf in `./reading_list/` alphabetically. This is my preferred ordering, but you can game it by appending numbers to the beginning of the pdf name (i.e. `1_*.pdf`) or by changing the code in `main.py`. As I encounter things I want to read I just drop the pdf into the reading list folder and go about my day.

If there's a response to the email, then the pdf will be removed from `./reading_list/` and moved to the `./notes/` directory along with the notes in the response. You can respond several times and it will append the new notes to the notes file.

I set up a new gmail account to send the emails (you must enable imap and disable security settings). The credentials for the account are stored in a file `credentials` (see `credentials-example` for an example).


To get daily messages I use system services to run the scripts `check_script.sh` and `send_script.sh` at regular intervals. `check_script.sh` waits for the network to connect and then runs `python3 main.py --check`. The `send_script.sh` script also waits for the network to wake up, then runs `python3 main.py --send`.

On Linux you can use `anacron` (or `cron`) to run these scripts at regular intervals. On MacOS you can use the launchd/launchctl system to run things ([this site](http://launched.zerowidth.com/) is helpful in making the complicated plists). I have no idea how to do this on Windows. I set mine up to run the check script every 2 hours and the send script every morning at 8am.
