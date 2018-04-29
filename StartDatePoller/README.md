# Simple START Registration Optimizer

This script automatically polls the START registration event server until registration is open, then refreshes the events displayed without reloading the page. Hopefully this results in less hassle when gunning for a desired START registration date.

## How to use:
1. Follow [this youtube video](https://youtu.be/8SDnX5hcMb0) to after signing into the "events list" page (~1:20)
2. Enter a search term (anything works) into the "Search by title" box and hit enter to search
3. Watch as the page begins to decend into madness
4. Refresh the page
5. You should get a page that looks [like this](https://i.imgur.com/tzvPf4E.png). The script will throw an error if you are not on the correct page, so double check to be sure.
6. Open chrome developer tools by pressing Ctrl+Shift+I
7. Paste the [script found here](https://raw.githubusercontent.com/db-dropDatabase/PythonWorkspace/master/StartDatePoller/mimified.js) (Ctrl+A then Ctrl+C to copy) into the developer console (usually found by clicking the "Console" tab next to "Elements" tab at the top of the developer tools window) and press Enter to run it
8. Once the script has detected that START registration is open, the page will load all the events, allowing you to proceed with registration normally (more details on how to finish registration in the youtube video above)