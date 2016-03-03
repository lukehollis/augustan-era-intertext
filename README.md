An example module demonstrating one possible usage of the CLTK text_reuse module to study intertextuality in Augustan Era poets writing in Latin.

This module assumes you've already downloaded the Latin corpora via the CLTK corpora downloader.  You will also need a local install of MongoDB and Python 3.5.

In order to start working with the text from the database, you will need to run the perseus_to_mongo.py script.  This will ingest all the XML documents in the greek_text_perseus and latin_text_perseus repositories downloaded by the CLTK into a local Mongo database named "perseus_corpora".

Next, to run the application using the CLTK text_reuse module to study intertextuality, run the intertext.py script.  This will run Levenshtein string distance comparisons between the documents retrieved from the author list specified at the top of intertext.py, using the compare_sliding_window method.
