import pdb
from concurrent import futures
from db import mongo
from cltk.text_reuse.text_reuse import TextReuse


AUTHORS = ["P. Vergilius Maro", "M. Annaeus Lucanus", "Sextus Propertius", "Martial", "Statius, P. Papinus", "Catullus", "Q. Horatius Flaccus (Horace)"]


class Intertext:

    def __init__(self, authors, text_dbname, comparison_dbname, n_processes=1, significance_threshold=0.5):
        self.authors = authors
        self.text_dbname = text_dbname
        self.comparison_dbname = comparison_dbname
        self.texts_to_compare = []
        self.n_processes = n_processes
        self.significance_threshold = significance_threshold

        return

    def load_texts(self):
        """Load works from the selected authors"""

        db = mongo(self.text_dbname)

        print("Loading texts:")
        # For each other, query the text database and add their works to texts to compare
        for author in self.authors:
            for text in db.texts.find({'author':author, 'language':"latin"}, no_cursor_timeout=True):
                self.texts_to_compare.append(text)
            print(" -- loaded texts for", author)

        return


    def compare_texts(self):
        """Compare the self.texts_to_compare with multiprocessing"""

        print("Comparing texts:")
        # For each text to compare, compare it to every other text to compare besides itself
        for i, text_a in enumerate(self.texts_to_compare):
            if self.n_processes > 1:
                # Create the process pool with the set number of processes
                executor = futures.ProcessPoolExecutor(self.n_processes)

                # Create the queue of tasks to be run
                futures_queue = [executor.submit(
                                        self._compare_texts, text_a, text_b ) for j, text_b in enumerate(self.texts_to_compare) if i != j
                                        ]

                # Wait for tasks to be run
                futures.wait(futures_queue)

            else:
                for j, text_b in enumerate(self.texts_to_compare):
                    # Don't compare the text to itself
                    if i != j:
                            self._compare_texts(text_a, text_b)


    def _compare_texts(self, text_a, text_b):
        """Compare two texts and save the comparisons to the db"""

        text_ref_a = {
                        'author' : text_a['author'],
                        'language' : text_a['language'],
                        'work' : text_a['title']
                    }
        text_ref_b = {
                        'author' : text_b['author'],
                        'language' : text_b['language'],
                        'work' : text_b['title']
                    }

        print(" -- comparing", text_a['author'], text_a['title'], "to", text_b['author'], text_b['title'])

        # Instantiate new TextReuse with metadata about both texts being compared
        t = TextReuse(text_ref_a, text_ref_b)

        # Create comparisons from both texts
        comparisons = t.compare_sliding_window(text_a['text'], text_b['text'])

        # Save the comparisons to the self.comparisons_dbname database
        self._save_comparisons(comparisons)

        return


    def export_comparisons(self):
        """Print out counts of comparisons per author for comparisons above the significance_threshold"""
        print("Exporting comparisons:")

        return


    def _save_comparisons(self, comparisons):
        """Save the comparisons to the database to be queried later"""
        db = mongo(self.comparison_dbname)
        count = 0


        # For each comparison, save it to the database
        for comparison_list in comparisons:
            for comparison in comparison_list:
                if comparison.ratio > self.significance_threshold:
                    count += 1
                    db.comparisons.insert({
                                            'str_a' : comparison.str_a,
                                            'str_b' : comparison.str_b,
                                            'ratio' : comparison.ratio,
                                            'author_a' : comparison.author_a,
                                            'author_b' : comparison.author_b,
                                            'work_a' : comparison.work_a,
                                            'work_b' : comparison.work_b,
                                            'subwork_a' : comparison.subwork_a,
                                            'subwork_b' : comparison.subwork_b,
                                            'text_n_a' : comparison.text_n_a,
                                            'text_n_b' : comparison.text_n_b,
                                            'language_a' : comparison.language_a,
                                            'language_b' : comparison.language_b
                                        })

        print(" -- -- saved", count, "comparisons")

        return

if __name__ == "__main__":
    text_dbname = "perseus_corpora"
    comparison_dbname = "augustan_era_intertext"

    # Example workflow:
    i = Intertext(AUTHORS, text_dbname, comparison_dbname, 5)
    i.load_texts()
    i.compare_texts()
    i.export_comparisons()
