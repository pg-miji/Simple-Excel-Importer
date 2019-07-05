import mysql.connector
import glob
import os
import json

from Dao import Dao
from Connector import Connector

path = "./json/"
parentCategoryNames = []

for folder in os.listdir(path):
       if os.path.isdir(path + folder):
              parentCategoryNames.append(folder)

connect = Connector().get()
cursor = connect.cursor()
dao = Dao

for parentCategoryName in parentCategoryNames:

       for p in glob.glob(path + parentCategoryName + '/*.json', recursive=True):
              if os.path.isfile(p):
                     childCategoryName = os.path.basename(p).replace('.json', '')

                     try:
                         parentCategoryCode = dao.getParentCategoryCode(cursor, parentCategoryName)
                         childCategoryCode = dao.getChildCategoryCode(cursor, parentCategoryCode, childCategoryName)
                         if childCategoryCode is None:
                                print (childCategoryName + ' not found.')

                         file = open(path + parentCategoryName + '/' +childCategoryName + '.json')
                         string = json.loads(file.read())

                         for book in string:

                                comment = book['comment']
                                if comment is None:
                                       continue

                                bookCode = dao.getBookCode(cursor, childCategoryCode, book['name'])
                                if bookCode is None:
                                    continue

                                existsSameComment = False
                                existingComments = dao.findExistingBookComments(cursor, bookCode)
                                if existingComments is not None:
                                    for existingComment in existingComments:
                                        if str(existingComment[0]).strip == str(comment).strip:
                                            existsSameComment = True

                                if existsSameComment == True:
                                    continue

                                dao.insertBookComment(cursor, bookCode, comment)
                                connect.commit()

                     except (mysql.connector.errors.ProgrammingError) as e:
                         print (e)
