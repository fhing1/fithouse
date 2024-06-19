from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'abcdefg'
CORS(app)


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='fit_db',
        auth_plugin='mysql_native_password'
    )


def execute_query(query, params=None, fetch=False):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    result = None
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        if fetch:
            result = cur.fetchall()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cur.close()
        db.close()
    return result


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        user = request.form.get('username')
        pwd = request.form.get('password')

        if not user or not pwd:
            return render_template('login.html', error='用户名或密码不能为空')

        connect = get_db_connection()
        cur = connect.cursor()
        cur.execute('SELECT * FROM Administrators WHERE username=%s AND password=%s', (user, pwd))
        users = cur.fetchone()
        cur.close()
        connect.close()

        if users:
            session['username'] = user
            return redirect(url_for('manage'))
        else:
            return render_template('login.html', error='用户名或密码错误')

    except Exception as e:
        return render_template('login.html', error=str(e))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/manage', methods=['GET'])
def manage():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('manage.html')


@app.route('/manage/worker/show', methods=['GET'])
def worker_show():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        workers = get_workers()
        if workers is not None:
            formatted_workers = format_workers_date(workers)
            return jsonify({'success': True, 'workers': formatted_workers}), 200
        else:
            return jsonify({'success': False, 'message': '获取工作人员信息失败'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


def get_workers():
    query = "SELECT * FROM worker"
    return execute_query(query, fetch=True)


def format_workers_date(workers):
    for worker in workers:
        worker['Birth'] = worker['Birth'].strftime("%Y-%m-%d")
        worker['WorkTime'] = worker['WorkTime'].strftime("%Y-%m-%d")
    return workers


@app.route('/manage/worker/add', methods=['GET', 'POST'])
def worker_add():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('worker_add.html')

    if request.method == 'POST':
        try:
            workername = request.form.get('WorkName')
            birth = request.form.get('Birth')
            sex = request.form.get('Sex')
            phone = request.form.get('Phone')
            job = request.form.get('Job')
            worktime = request.form.get('WorkTime')
            if add_worker(workername, birth, sex, phone, job, worktime):
                return redirect(url_for('manage'))
            else:
                return jsonify({'success': False, 'error': '添加失败，请重试或联系管理员'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400


def add_worker(workername, birth, sex, phone, job, worktime):
    query = "INSERT INTO worker (WorkerName, Birth, Sex, Phone, Job, WorkTime) VALUES (%s, %s, %s, %s, %s, %s)"
    params = (workername, birth, sex, phone, job, worktime)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False


@app.route('/manage/worker/delete', methods=['GET', 'POST'])
def worker_del():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('worker_delete.html')

    if request.method == 'POST':
        worker_name = request.form.get('workerName')
        worker_time = request.form.get('workerTime')

        if not worker_name or not worker_time:
            return jsonify({'success': False, 'error': '缺少姓名或入职时间'}), 400

        try:
            if del_worker(worker_name, worker_time):
                return redirect(url_for('manage'))
            else:
                return jsonify({'success': False, 'error': '删除失败，请重试或联系管理员'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500


def del_worker(workername, worktime):
    query = "DELETE FROM worker WHERE WorkerName = %s AND WorkTime= %s"
    params = (workername, worktime)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False


@app.route('/manage/worker/update', methods=['GET', 'POST'])
def worker_update():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('worker_update.html')

    if request.method == 'POST':
        worker_name = request.form.get('WorkerName')
        birth = request.form.get('Birth')
        sex = request.form.get('Sex')
        phone = request.form.get('Phone')
        job = request.form.get('Job')
        worktime = request.form.get('WorkTime')

        if not all([worker_name, birth, sex, phone, job, worktime]):
            return jsonify({'success': False, 'error': '表单项不完整'}), 400

        if update_worker(worker_name, birth, sex, phone, job, worktime):
            return redirect(url_for('manage'))
        else:
            return jsonify({'success': False, 'error': '更新失败，请重试或联系管理员'}), 500


def update_worker(worker_name, birth, sex, phone, job, worktime):
    query = "UPDATE worker SET Birth=%s, Sex=%s, Phone=%s, Job=%s, WorkTime=%s WHERE WorkerName = %s"
    params = (birth, sex, phone, job, worktime, worker_name)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False

@app.route('/manage/member/show', methods=['GET'])
def member_show():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        members = get_members()
        if members is not None:
            formatted_members = format_members_date(members)
            return jsonify({'success': True, 'members': formatted_members}), 200
        else:
            return jsonify({'success': False, 'message': '获取会员信息失败'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
def get_members():
    query = "SELECT * FROM members"
    return execute_query(query, fetch=True)
def format_members_date(members):
    for member in members:
        member['Birth'] = member['Birth'].strftime("%Y-%m-%d")
        member['RegisterDate'] = member['RegisterDate'].strftime("%Y-%m-%d")
    return members

@app.route('/manage/member/add', methods=['GET', 'POST'])
def member_add():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('member_add.html')

    if request.method == 'POST':
        try:
            member_id = request.form.get('MemberID')
            member_name = request.form.get('MemberName')
            birth = request.form.get('Birth')
            register_date = request.form.get('RegisterDate')
            sex = request.form.get('Sex')
            phone = request.form.get('Phone')
            height = request.form.get('Height')
            weight = request.form.get('Weight')

            # 注意这里函数名和参数应与实际定义的add_member函数匹配
            if add_member(member_id, member_name, birth, register_date, sex, phone, height, weight):
                return redirect(url_for('manage'))  # 假设'manage_members'是管理会员页面的路由
            else:
                return jsonify({'success': False, 'error': '添加失败，请重试或联系管理员'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400


def add_member(member_id, member_name, birth, register_date, sex, phone, height, weight):
    # 更新SQL语句以匹配会员表的字段名，并修正参数列表
    query = "INSERT INTO members (MemberID, MemberName, Birth, RegisterDate, Sex, Phone, Height, Weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    params = (member_id, member_name, birth, register_date, sex, phone, height, weight)
    try:
        # 执行查询
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        # 打印错误信息
        print("Error: ", e)
        return False

@app.route('/manage/member/delete', methods=['GET', 'POST'])
def member_del():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('member_delete.html')  # 确保有对应的member_delete.html模板

    if request.method == 'POST':
        member_id = request.form.get('memberID')
        register_date = request.form.get('registerDate')

        if not member_id or not register_date:
            return jsonify({'success': False, 'error': '缺少会员卡号或办卡日期'}), 400

        try:
            if del_member(member_id, register_date):
                return redirect(url_for('manage')),200  # 假设'manage_members'是管理会员的页面
            else:
                return jsonify({'success': False, 'error': '删除失败，请重试或联系管理员'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500


def del_member(member_id, register_date):
    query = "DELETE FROM members WHERE MemberID = %s AND RegisterDate = %s"  # 假设members是会员表
    params = (member_id, register_date)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False

@app.route('/manage/member/update', methods=['GET', 'POST'])
def member_update():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('member_update.html')  # 更改模板文件名以匹配会员更新

    if request.method == 'POST':
        member_id = request.form.get('MemberID')
        birth = request.form.get('Birth')
        sex = request.form.get('Sex')
        phone = request.form.get('Phone')
        height = request.form.get('Height')
        weight = request.form.get('Weight')

        if not all([member_id, birth, sex, phone, height, weight]):
            return jsonify({'success': False, 'error': '表单项不完整'}), 400

        if update_member(member_id, birth, sex, phone, height, weight):
            return redirect(url_for('manage'))
        else:
            return jsonify({'success': False, 'error': '更新失败，请重试或联系管理员'}), 500


def update_member(member_id, birth, sex, phone, height, weight):
    query = "UPDATE members SET Birth=%s, Sex=%s, Phone=%s, Height=%s, Weight=%s WHERE MemberID = %s"
    params = (birth, sex, phone, height, weight, member_id)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False

@app.route('/manage/course/show', methods=['GET'])
def courser_show():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        courses = get_courses()
        if courses is not None:
            return jsonify({'success': True, 'courses': courses}), 200
        else:
            return jsonify({'success': False, 'message': '获取会员信息失败'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
def get_courses():
    query = "SELECT * FROM courses"
    return execute_query(query, fetch=True)

@app.route('/manage/course/add', methods=['GET', 'POST'])
def course_add():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('course_add.html')

    if request.method == 'POST':
        try:
            CourseID = request.form.get('CourseID')
            CourseName = request.form.get('CourseName')
            TrainingLocation = request.form.get('TrainingLocation')
            CourseTime = request.form.get('CourseTime')
            CourseCoach = request.form.get('CourseCoach')

            if add_course(CourseID, CourseName, TrainingLocation, CourseTime, CourseCoach):
                return redirect(url_for('manage'))
            else:
                return jsonify({'success': False, 'error': '添加失败，请重试或联系管理员'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

def add_course(CourseID, CourseName, TrainingLocation, CourseTime, CourseCoach):
    # 更新SQL语句以匹配会员表的字段名，并修正参数列表
    query = "INSERT INTO courses (CourseID, CourseName, TrainingLocation, CourseTime, CourseCoach) VALUES (%s, %s, %s, %s, %s)"
    params = (CourseID, CourseName, TrainingLocation, CourseTime, CourseCoach)
    try:
        # 执行查询
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        # 打印错误信息
        print("Error: ", e)
        return False


@app.route('/manage/course/delete', methods=['GET', 'POST'])
def course_del():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('course_delete.html')

    if request.method == 'POST':
        CourseID = request.form.get('CourseID')

        CourseName = request.form.get('CourseName')

        if not CourseName or not CourseID:
            return jsonify({'success': False, 'error': '缺少课程编号或课程名称'}), 400

        try:
            if del_course(CourseID, CourseName):
                return redirect(url_for('manage')),200
            else:
                return jsonify({'success': False, 'error': '删除失败，请重试或联系管理员'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500


def del_course(CourseID, CourseName):
    query = "DELETE FROM courses WHERE CourseID = %s AND CourseName= %s"
    params = (CourseID, CourseName)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False


@app.route('/manage/course/update', methods=['GET', 'POST'])
def course_update():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('course_update.html')  # 更改模板文件名以匹配会员更新

    if request.method == 'POST':
        CourseID = request.form.get('CourseID')
        CourseName = request.form.get('CourseName')
        TrainingLocation = request.form.get('TrainingLocation')
        CourseTime = request.form.get('CourseTime')
        CourseCoach = request.form.get('CourseCoach')
        # CourseID CourseName TrainingLocation CourseTime CourseCoach

        if not all([CourseID,CourseName,TrainingLocation,CourseTime,CourseCoach]):
            return jsonify({'success': False, 'error': '表单项不完整'}), 400

        if update_course(CourseID,CourseName,TrainingLocation,CourseTime,CourseCoach):
            return redirect(url_for('manage'))
        else:
            return jsonify({'success': False, 'error': '更新失败，请重试或联系管理员'}), 500


def update_course(CourseID,CourseName,TrainingLocation,CourseTime,CourseCoach):
    query = "UPDATE courses SET CourseName=%s,TrainingLocation=%s,CourseTime=%s,CourseCoach=%s WHERE CourseID=%s"
    params = (CourseName,TrainingLocation,CourseTime,CourseCoach,CourseID)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False

@app.route('/manage/equipment/show', methods=['GET'])
def equipment_show():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        equipments = get_equipments()
        if equipments is not None:
            return jsonify({'success': True, 'workers': equipments}), 200
        else:
            return jsonify({'success': False, 'message': '获取工作人员信息失败'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


def get_equipments():
    query = "SELECT * FROM equipments"
    return execute_query(query, fetch=True)

@app.route('/manage/equipment/add', methods=['GET', 'POST'])
def equipment_add():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('equipment_add.html')

    if request.method == 'POST':
        try:
            EquipmentName = request.form.get('EquipmentName')
            TrainingLocation = request.form.get('TrainingLocation')
            if add_equipment(EquipmentName,TrainingLocation):
                return redirect(url_for('manage'))
            else:
                return jsonify({'success': False, 'error': '添加失败，请重试或联系管理员'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400


def add_equipment(EquipmentName,TrainingLocation):
    query = "INSERT INTO equipments (EquipmentName,TrainingLocation) VALUES (%s, %s)"
    params = (EquipmentName,TrainingLocation)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False

@app.route('/manage/equipment/delete', methods=['GET', 'POST'])
def equipment_del():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('equipment_delete.html')

    if request.method == 'POST':
        EquipmentID = request.form.get('EquipmentID')

        EquipmentName = request.form.get('EquipmentName')

        if not EquipmentName or not EquipmentID:
            return jsonify({'success': False, 'error': '缺少器材编号或器材名称'}), 400

        try:
            if del_equipment(EquipmentID, EquipmentName):
                return redirect(url_for('manage')),200
            else:
                return jsonify({'success': False, 'error': '删除失败，请重试或联系管理员'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500


def del_equipment(EquipmentID, EquipmentName):
    query = "DELETE FROM equipments WHERE EquipmentID = %s AND EquipmentName = %s"
    params = (EquipmentID, EquipmentName)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False
@app.route('/manage/equipment/update', methods=['GET', 'POST'])
def equipment_update():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('equipment_update.html')

    if request.method == 'POST':
        EquipmentID = request.form.get('EquipmentID')
        EquipmentName = request.form.get('EquipmentName')
        TrainingLocation = request.form.get('TrainingLocation')

        if not all([EquipmentID,EquipmentName,TrainingLocation]):
            return jsonify({'success': False, 'error': '表单项不完整'}), 400

        if update_equipment(EquipmentID,EquipmentName,TrainingLocation):
            return redirect(url_for('manage'))
        else:
            return jsonify({'success': False, 'error': '更新失败，请重试或联系管理员'}), 500


def update_equipment(EquipmentID,EquipmentName,TrainingLocation):
    query = "UPDATE equipments SET EquipmentName=%s,TrainingLocation=%s WHERE EquipmentID=%s"
    params = (EquipmentName,TrainingLocation,EquipmentID)
    try:
        execute_query(query, params)
        return True
    except mysql.connector.Error as e:
        print("Error: ", e)
        return False
if __name__ == '__main__':
    app.run(debug=True, port=8000)
