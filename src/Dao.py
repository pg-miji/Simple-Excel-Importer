from datetime import datetime

class Dao:

    def getParentCategoryCode(cursor, categoryName):

        sql = """
        SELECT
            code
        FROM
            parent_categories
        WHERE
            name = '%s'
        """

        cursor.execute(sql % categoryName)
        parentCategoryCode = cursor.fetchone()
        if parentCategoryCode is None:
            return
        else:
            return parentCategoryCode[0]


    def getChildCategoryCode(cursor, parentCategoryCode, childCategoryName):

        sql = """
        SELECT
            code
        FROM
            categories
        WHERE
            parent_category_code = %s
            AND name = %s
        """

        cursor.execute(sql, (parentCategoryCode, childCategoryName))
        childCategoryCode = cursor.fetchone()
        if childCategoryCode is None:
            return
        else:
            return childCategoryCode[0]


    def getBookCode(cursor, childCategoryCode, bookName):

        sql = """
        SELECT
            code
        FROM
            books
        WHERE
            child_category_code = %s
            AND name = %s
        """

        cursor.execute(sql, (childCategoryCode, bookName))
        bookCode = cursor.fetchone()
        if bookCode is None:
            return
        else:
            return bookCode[0]


    def findExistingBookComments(cursor, bookCode):

        sql = """
        SELECT
            contents
        FROM
            book_comments
        WHERE
            book_code = '%s'
        """

        cursor.execute(sql % bookCode)
        return cursor.fetchall()


    def insertBookComment(cursor, bookCode, bookComment):

        sql = """
        INSERT INTO 
            book_comments
        (
            book_code,
            contents,
            created_at
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """

        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        cursor.execute(sql, (bookCode, bookComment, now))
