gmail-size
-----------

Finds the big emails in your Gmail account.  Scans all your emails (that is,
every email in **All Mail**) and tags them with a corresponding label
**10MB-25MB**, **5MB-10MB**, **2MB-5MB** or **1MB-2MB**

### Usage ###

    gmail-size.py user@gmail.com


gmail-labelsize
----------------

Totals up the size of all messages associated with each of your Gmail labels.

### Usage ###

    gmail-labelsize.py user@gmail.com


gmail-searchsize
-----------------

Totals up the size of all messages resulting from a given Gmail search..

### Usage ###

    gmail-searchsize.py user@gmail.com "Gmail search"

### Example ###

    % gmail-searchsize.py user@gmail.com "has:attachment -filename:jpg"
    Password: 
    has:attachment filename:jpg           3.8GB
