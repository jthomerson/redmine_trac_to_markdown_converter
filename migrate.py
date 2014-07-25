from datetime import datetime
import MySQLdb
import yaml
from TracToMarkdownConverter import TracToMarkdownConverter

class Migrate:

   def __init__(self, config):
      self.config = config
      self.converter = TracToMarkdownConverter()


   def connect(self):
      return  MySQLdb.connect(host = "localhost",
                              user = self.config['dbuser'],
                              passwd = self.config['dbpass'],
                              db = self.config['dbname'])


   def convert(self):
      db = self.connect()
      cur = db.cursor()

      for table in self.config['fields']:
         fieldsList = self.config['fields'][table]

         fieldsList.insert(0, 'id')
         fields = ", ".join(fieldsList)

         query = "select %s from %s order by id desc" % (fields, table)
         cur.execute(query)

         for row in cur.fetchall():
            convertedRow = self.convertRow(fieldsList, row)
            if table == 'wiki_contents':
               # only update version number if the row has changed
               oldText = row[fieldsList.index('text')]
               if convertedRow['text'] != oldText:
                  version = self.insertWikiVersion(convertedRow, cur)
                  convertedRow['version'] = version
            elif table == 'issues':
               oldText = row[fieldsList.index('description')]
               if convertedRow['description'] != oldText:
                  self.insertJournal(oldText, convertedRow, cur)

            q = self.createUpdateSQL(table, convertedRow)
            cur.execute(q[0], q[1])
            db.commit()
      cur.close()


   def convertRow(self, fields, row):
      convertedRow = dict()
      for i, field in enumerate(row):
         if type(fields[i]) is not str:
            convertedField = field
         else:
            convertedField = self.convertField(field)
         convertedRow[fields[i]] = convertedField
      return convertedRow


   def convertField(self, field):
      return self.converter.convert(field)

   def createUpdateSQL(self, table, row):
      sql = 'update %s set ' % table
      values = []
      for k, v in row.iteritems():
         if k != 'id':
            sql += k + " = %s, "
            values.append(v)

      return (sql[:len(sql)-2] + ' where id = %d' % row['id'], values)


   def insertJournal(self, oldText, convertedRow, cur):
      journalSql = ("insert into journals "
                    "(journalized_id, journalized_type, user_id, notes, created_on) "
                    "values (%s, %s, %s, %s, %s)")
      notes = 'Trac to Markdown conversion'
      cur.execute(journalSql, (convertedRow['id'], 'Issue', self.config['author_id'], notes, datetime.now()))
      journal_id = cur.lastrowid

      journalDetailsSql = ("insert into journal_details "
                           "(journal_id, property, prop_key, old_value, value) "
                           "values (%s, %s, %s, %s, %s)")
      journalDetails = (journal_id, 'attr', 'description', oldText, convertedRow['description'])
      cur.execute(journalDetailsSql, journalDetails)


   def insertWikiVersion(self, row, cur):
      versionSql = 'select max(version) from wiki_content_versions where wiki_content_id = %s'
      cur.execute(versionSql, row['id'])
      version = cur.fetchone()
      version = 1 if not version else version[0] + 1

      sql = 'insert into wiki_content_versions (version, updated_on, comments, wiki_content_id, page_id, author_id, data) values (%s, %s, %s, %s, %s, %s, %s)'
      cur.execute(sql, [version, datetime.now(), "Trac to Markdown conversion", row['id'], row['id'], self.config['author_id'], row['text']])
      return version


def main():
   configFile = open('migrate.yml', 'r')
   configFile = configFile.read()
   config = yaml.load(configFile)
   migrate = Migrate(config)
   migrate.convert()


if __name__ == "__main__":
   main()
