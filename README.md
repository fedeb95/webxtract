# webxtract
Reconstruct (partially) website structure from wireshark plain text export file
Given `folder/plain.txt` a wireshark plain text capture file, run

`python webxtract.py folder/plain.txt`

to generate a folder `folder/output` with the reconstructed contents from the capture. 
This work only if HTTP packages are present. It tries (only tries) to substitute links in extracted files with other extracted files.
More contributions are needed to make it useful in this way. 

What it does well: strip away \t, \n, etc, and reconstruct directory structure. It's more easy to examine 
extracted content by opening everything in the browser.

Any help appreciated.
