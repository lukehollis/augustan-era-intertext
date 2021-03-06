An example module demonstrating one possible usage of the CLTK text_reuse module to study intertextuality in Augustan Era poets writing in Latin.

This module assumes you've already downloaded the Latin corpora via the CLTK corpora downloader.  You will also need a local install of MongoDB and Python 3.5.

In order to start working with the text from the database, you will need to run the perseus_to_mongo.py script.  This will ingest all the XML documents in the greek_text_perseus and latin_text_perseus repositories downloaded by the CLTK into a local Mongo database named "perseus_corpora".

Next, to run the application using the CLTK text_reuse module to study intertextuality, run the intertext.py script.  This will run Levenshtein string distance comparisons between the documents retrieved from the author list specified at the top of intertext.py, using the compare_sliding_window method.  Because the nature of string comparison is CPU intensive, the script relies on multiprocessing, spawning the number of processes specified in the n_processes parameter on the Intertext class.

When a process finishes comparing two documents, it will save all the comparisons created between the two documents if the two strings that are being compared are at or above the significance_threshold parameter set on the Intertext class.  I've arbitrarily chosen all comparisons with an edit distance ratio above a 0.6 as significant.  If you set the significance_threshold very low (e.g. 0), you will save large quantities of comparison data and should do small tests before letting the script run for long periods of time--or will be potentially in danger of running out of space on your hard drive.

The data generated by this module will be visualized with a chord diagram graph from the d3.js library.  
