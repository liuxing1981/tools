class Criteria:
    query = []
    @staticmethod
    def dateConverter(date):
        year, month, day = date.split('-')
        if len(month) == 1:
            month = '0' + month
        if len(day) == 1:
            day = '0' + day
        if (month == '01'):
            month = 'Jan'
        elif (month == '02'):
            month = 'Feb'
        elif (month == '03'):
            month = 'Mar'
        elif (month == '04'):
            month = 'Apr'
        elif (month == '05'):
            month = 'May'
        elif (month == '06'):
            month = 'Jun'
        elif (month == '07'):
            month = 'Jul'
        elif (month == '08'):
            month = 'Aug'
        elif (month == '09'):
            month = 'Sept'
        elif (month == '10'):
            month = 'Oct'
        elif (month == '11'):
            month = 'Nov'
        elif (month == '12'):
            month = 'Dec'
        return '%s-%s-%s' % (day, month, year)

    def addAnd(self, query):
        self.query.extend(query)
        # print(self.query)
        return self

    def addOr(self, query):
        temp = ['OR']
        temp += self.query
        temp.extend(query)
        self.query = [[]]
        self.query[0].append(temp)
        # print(self.query)
        return self

    def getQuery(self):
        return self.query

    def findAll(self):
        return ['all']

    def findByDate(self, date):
        date = Criteria.dateConverter(date)
        return ['ON', date]

    def findByDateFrom(self,date):
        date = Criteria.dateConverter(date)
        return ['SINCE', date]

    def findByDateBetween(self, fromDate, toDate):
        fromDate = Criteria.dateConverter(fromDate)
        toDate = Criteria.dateConverter(toDate)
        return ['SINCE',fromDate,'BEFORE',toDate]

    def findBySenders(self, *senders):
        query = []
        if(len(senders) == 1):
            query.append('FROM')
            query.append(senders[0])
        else:
            query.append('OR')
            for sender in senders:
                query.append('FROM')
                query.append(sender)
        return query

    def findBySubject(self, subject):
        return ['SUBJECT',subject]

    def findByContent(self, content):
        return ['TEXT','"%s"'%content]