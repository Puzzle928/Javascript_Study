import cx_Oracle
from dto import EmpDTO
import json
import collections # 데이터를 어떤 구조로 관리할 것인가를 의미하는 자료구조를 지원하는 library


class EmpDAO:
    def empdelete(self, dto):
        conn = cx_Oracle.connect(user="SCOTT", password="TIGER", dsn="xe")
        cur = conn.cursor()

        cur.execute("delete from emp01 where empno=:empno",
                    empno=dto.getEmpno())
        conn.commit()

        cur.close()
        conn.close()

    def empupdate(self, dto):
        conn = cx_Oracle.connect(user="SCOTT", password="TIGER", dsn="xe")
        cur = conn.cursor()

        cur.execute("update emp01 set ename=:ename, sal=:sal where empno=:empno",
                    ename=dto.getEname(), empno=dto.getEmpno(), sal=dto.getSal())
        conn.commit()

        cur.close()
        conn.close()

    # 한명의 직원 등록

    def empinsert(self, dto):    # EmpDTO 객체를 통으로 매개변수 값으로 받을 예정
        # insert into emp01 values (1234, 'test', 200);
        conn = cx_Oracle.connect(user="SCOTT", password="TIGER", dsn="xe")
        cur = conn.cursor()

        try:
            cur.execute("insert into emp01 values (:empno, :ename, :sal)",
                        empno=dto.getEmpno(), ename=dto.getEname(), sal=dto.getSal())
            print("------------")
            conn.commit()
        except Exception as e:
            print(e)

        finally:
            cur.close()
            conn.close()

    # 한명의 직원 정보 반환
    def empone(self, empno):

        data = ''

        try:
            conn = cx_Oracle.connect(user="SCOTT", password="TIGER", dsn="xe")
            cur = conn.cursor()
            cur.execute("select * from emp01 where empno=:v", v=empno)
            row = cur.fetchone()
            data = '{"ename":"' + row[1] + '", "sal":' + str(row[2]) + '}'

        except Exception as e:
            print(e)

        finally:
            cur.close()
            conn.close()

        return data

    def empall(self):
        data = ''

        try:
            conn = cx_Oracle.connect(user="SCOTT", password="TIGER", dsn="xe")
            cur = conn.cursor()
            cur.execute("select * from emp01")
            rows = cur.fetchall()
            # json 포멧으로 가공 : empno/enmae/sal key ; json 배열
            # 다양한 방법
            v = []
            for row in rows:
                d = collections.OrderedDict()
                d['empno'] = row[0]
                d['ename'] = row[1]
                d['sal'] = row[2]

                v.append(d)

            data = json.dumps(v, ensure_ascii=False)

            return data
                

        except Exception as e:
            print(e)

        finally:
            cur.close()
            conn.close()

        return data
if __name__ == "__main__":
    dao = EmpDAO()
    # dto = EmpDTO(2, 't', 20)
    dao.empall()


''' 
dao.py의 모든 코드들은 app.py에서 호출해서 사용
단 구현시에 제대로 구현하는지 구현 로직별로 확인
단위 test 지칭

방법 : 파일단위(모듈)별로 실행가능하게 if __name__ == "__main__":
py 파일 독립적으로 실행 가능하게 해주는 독립실행 코드
'''
