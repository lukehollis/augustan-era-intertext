import pdb
import os, json, re
from bs4 import BeautifulSoup
import html.parser
import pymongo
from db import mongo

class PerseusToMongo:
# a class to migrate Perseus XML file data to mongo db

	def __init__(self):
		self.data_dirs = [
								os.path.join(os.path.expanduser("~"), 'cltk_data/greek/text/greek_text_perseus'),
								os.path.join(os.path.expanduser("~"), 'cltk_data/latin/text/latin_text_perseus')
							]
		self.import_db = 'perseus_corpora_updated'

		# empty the text collection
		db = mongo(self.import_db)
		db.texts.remove()

		return

	def migrate_xml(self):
	# migrate the Perseus xml to mongo
		print(' - Migrating XML')

		for data_dir in self.data_dirs:
			for path, subdirs, fnames in os.walk(data_dir):

				for fname in fnames:
					froot_name, fext = os.path.splitext(fname)
					if fext == ".xml":
						print(' -- importing', fname)
						root = self._open_text(os.path.join(path, fname))
						text_data = self._parse_tei_xml(root)
						self._save_to_mongo(text_data)

		return

	def _open_text(self, fname):
	# open and parse the contents of an xml file

		print(' --', fname)

		with open(fname, 'r') as xml_file:

			# open file as string for preprocessing
			data = xml_file.read().replace('\n',' ')

			# unescape html chars
			html_parser = html.parser.HTMLParser()
			data = html_parser.unescape(data)

			# parse data
			root = BeautifulSoup(data)

		return root

	def _parse_tei_xml(self, root):
	# parse tei xml to select data model based on migration type

		text_data = {}

		text_data = {
				'title': '',
				'author': '',
				'language': '',
				'text': ''
			}

		try:
			text_data['title'] = root.title.text.strip()

		except:
			print(" -- -- title not found")
			pass

		try:
			text_data['author'] = root.author.text.strip()

		except:
			print(" -- -- author not found")
			pass

		try:
			text_data['language'] = root.language.text.strip().lower()

		except:
			print(" -- -- language not found")
			pass

		try:
			text_data['text'] = root.body.text

		except:
			print(" -- -- body not found")
			pass



		return text_data

	def _save_to_mongo(self, text_data):
	# finally, insert the object into mongo

		db = mongo(self.import_db)
		db.texts.insert(text_data)

		return


if __name__ == "__main__":
	print('-------------------------------------')
	print('Migrating Perseus XML to MongoDB:')
	print('-------------------------------------')
	ptm = PerseusToMongo()
	ptm.migrate_xml()
