import Sheets as sheets

statusList = ['Просмотрено', 'Запланировано', 'Отклонено']
placeList = ['Дискорд', 'Прочее']


class Table:
    def __init__(self):
        self.sizeDown = sheets.getLastColumn()
        self.sizeRight = sheets.getLastRow()
        self.films = []
        self.users = []
        self.updateTable()
        # rowPos = 'abcdefghijklmnopqrstuvwxyz'
        # usersList = sheets.getRowsValues('G', rowPos[self.sizeRight - 1], 3)
        # # filmsList = sheets.getColumnValues('A', 4, self.sizeDown) probably doesnt need it
        #
        # # for i in range(6, self.sizeRight):
        # #     tmpColumn = sheets.getColumnValues(rowPos[i], )
        #
        # # this is tmp solution
        # # users must fill first because in films author = User.name
        # for i in range(6, self.sizeRight):
        #     self.users.append(User(rowPos[i], usersList[i - 6], i))
        #
        # for i in range(4, self.sizeDown + 1):
        #     tmpRow = sheets.getRowsValues('A', 'F', i)
        #     if tmpRow[0].strip():
        #         self.films.append(
        #             Film(i, tmpRow[0], tmpRow[5], tmpRow[3], tmpRow[4], status=tmpRow[1], place=tmpRow[2]))

    def updateTable(self):
        self.sizeDown = sheets.getLastColumn()
        self.sizeRight = sheets.getLastRow()
        rowPos = 'abcdefghijklmnopqrstuvwxyz'
        usersList = sheets.getRowsValues('G', rowPos[self.sizeRight - 1], 3)

        tmpUserList = []
        for i in range(6, self.sizeRight):
            tmpUserList.append(User(rowPos[i], usersList[i - 6], i))
        self.users = tmpUserList

        tmpFilmsList = []
        for i in range(4, self.sizeDown + 1):
            tmpRow = sheets.getRowsValues('A', 'F', i)
            if tmpRow is not None:
                tmpFilmsList.append(
                    Film(i, tmpRow[0], tmpRow[5], tmpRow[3], tmpRow[4], status=tmpRow[1], place=tmpRow[2]))
        self.films = tmpFilmsList

    def getAllFilms(self):
        names = []
        for film in self.films:
            names.append(film.name)
        return names

    def getPlannedFilms(self):
        names = []
        for film in self.films:
            if film.status == 'Запланировано':
                names.append(film.name)
        return names

    def getUserNames(self):
        names = []
        for user in self.users:
            names.append(user.name)
        return names

    def getSoonestFilm(self):
        for film in self.films:
            if film.status == 'Запланировано':
                return film

    def getWatchedFilms(self):
        watchedFilms = []
        for film in self.films:
            if film.status == 'Просмотрено':
                watchedFilms.append(film)
        return watchedFilms

    def getFilm(self, name):
        list = []
        for film in self.films:
            fileName = str.lower(film.name)
            if fileName.find(str.lower(name)):
                list.append(film)
        if not list:
            return None
        else:
            return list
    # def addNewFilm
    # def addNewUser
    # def changeDescriptionByName
    # def changeFilmStatusByName
    # def changeSoonestFilmStatus
    # def getFilmRateByName
    # def rateFilmByUser
    # def addCommentByUser


class Film:
    def __init__(self, pos, name, rate, author, description, status='Запланировано', place='Дискорд'):
        self.pos = pos
        self.name = name  # A
        self.rate = rate  # F
        self.place = place  # C
        self.author = author  # D
        self.status = status  # B
        self.description = description  # E

    def pushChanges(self):
        # name
        cell = 'A' + str(self.pos)
        sheets.setCellValue(cell, self.name)
        # status
        cell = 'B' + str(self.pos)
        sheets.setCellValue(cell, self.status)
        # place
        cell = 'C' + str(self.pos)
        sheets.setCellValue(cell, self.place)
        # author
        cell = 'D' + str(self.pos)
        sheets.setCellValue(cell, self.author)
        # description
        cell = 'E' + str(self.pos)
        sheets.setCellValue(cell, self.description)


class User:
    def __init__(self, pos, name, discId):
        self.pos = pos  # letter
        self.name = name
        self.descId = discId
        # self.rates = {}  # {'filmName': 8,0}
        # self.comments = {}  # {'filmName: 'comment'}

    def pushChanges(self):
        # name
        cell = self.pos + 3
        sheets.setCellValue(cell, self.name)
