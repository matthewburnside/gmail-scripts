gmail\_size
-----------

Finds the big emails in your Gmail account.  Scans all your emails (that is,
every email in **All Mail**) and tags them with a corresponding label
**10MB-25MB**, **5MB-10MB** **2MB-5MB** or **1MB-2MB**

### Usage ###

    gmail_size.py user@gmail.com


gmail\_labelsize
----------------

Totals up the size of all messages associated with each of your Gmail labels.

### Usage ###

    gmail_labelsize.py user@gmail.com


gmail\_searchsize
-----------------

Totals up the size of all messages resulting from a given Gmail search..

### Usage ###

    gmail_searchsize.py user@gmail.com "Gmail search"

### Example ###

    gmail_searchsize.py user@gmail.com "has:attachment -cheese"
    
