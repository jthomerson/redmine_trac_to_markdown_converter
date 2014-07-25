import migrate
import unittest
import yaml

class MigrateTest(unittest.TestCase):
   def setUp(self):
      configFile = open('migrate.yml', 'r')
      configFile = configFile.read()
      config = yaml.load(configFile)
      self.migration = migrate.Migrate(config)
      fixtureFile = open('migrateTest.yml', 'r')
      fixtureFile = fixtureFile.read()
      self.fixtures = yaml.load(fixtureFile)

   def test_converts_to_markdown(self):
      for fixture in self.fixtures['testCases']:
         convertedField = self.migration.convertField(fixture['testCase']['test'])
         self.assertEquals(fixture['testCase']['expected'], convertedField)

if __name__ == '__main__':
   unittest.main()
