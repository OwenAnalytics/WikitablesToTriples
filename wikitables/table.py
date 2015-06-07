from bs4 import BeautifulSoup
from wikitables.sparql import getPredicates

class Table:

    """This class abstracts tables in Wikipedia articles to provide additional extraction functionality."""

    def __init__(self, soup):
        self.soup = soup
        self.caption = soup.find('caption')
        self.head = soup.find('thead')
        self.body = soup.find('tbody')
        self.section = self._section()
        self.columnNames = [th.text for th in self.soup.findAll('tr')[0].findAll('th')]
        self.rows = [tr.findAll('td') for tr in self.soup.findAll('tr') if tr.find('td')]

    def __repr__(self):
        if self.caption:
            return self.caption.text
        return "Unnamed table in section \'%s\'" % self.section

    def _section(self):
        """Try finding first header (h2) before table.
        If none found, use the article's title."""
        for sibling in self.soup.previous_siblings:
            if sibling.name == 'h2':
                return sibling.span.text

        for parent in self.soup.parents:
            if parent.has_attr('id') and parent['id'] == 'content':
                return parent.h1.text

    def peek(self, chars=400):
        return self.soup.prettify()[:chars]

    def asDictionary(self, text=False):
        columnDict = {}
        for i, c in enumerate(self.columnNames):
            columnDict[c] = [str(row[i]) if text else row[i] for row in self.rows]
        return columnDict

    @property
    def columns(self):
        columns = []
        for i, c in enumerate(self.columnNames):
            columns.append([row[i] for row in self.rows])
        return columns

    def row(self, i):
        return self.rows[i]

    def column(self, key):
        i = key if type(key) is int else self.columnNames.index(key)
        return [row[i] for row in self.rows]

    def skipTable(self):
        # Skip tables with rowspan/colspan
        return True in [td.has_attr('colspan') or td.has_attr('rowspan') for td in self.soup.findAll('td')]

    def getPredicatesForColumns(self, fromColumn, toColumn):
        fromData = self.column(fromColumn)
        toData = self.column(toColumn)
        valueStore = dict()
        for i in range(0, len(fromData)):
            fromContent, check = self.getContent(fromData[i])
            toContent, _ = self.getContent(toData[i])

            if check:
                for predicate in getPredicates(fromContent, toContent):
                    if predicate in valueStore:
                        valueStore[predicate] += 1
                    else:
                        valueStore[predicate] = 1

        return valueStore

    def getContent(self, cell):
        link = cell.find('a', href = True)
        if not link:
            literal = list(cell.strings)[0]
            return literal, False
        else:
            return link['href'].replace('/wiki', '<http://dbpedia.org/resource') + '>', True




    # def populateRows(self):
    #     trs = [tr.findAll('td') for tr in self.soup.findAll('tr') if tr.find('td')]
    #     rowLength = len(max(trs, lambda tr: len(tr)))
    #     rows = [[None for cell in range(0, rowLength)] for tr in trs]
    #
    #     for row, tr in enumerate(trs):
    #         col = 0
    #         for td in tr:
    #             while not rows[row][col]: col += 1
    #             rows[row][col] = td
    #
    #     return rows