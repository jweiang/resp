# -*- coding: utf-8 -*-
#!/usr/bin/env python
#link---joy
#version 1.0 2015-09-08

import os
import MySQLdb
import time
import re
import json

def mysql_ML(slt):
        conn= MySQLdb.connect(
        host='',
        port = 3306,
        user='',
        passwd='',
        db ='',
        )
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
	cur.execute("set names utf8;")
        sltresult=cur.execute(slt)
        SL = cur.fetchmany(sltresult)
        cur.close()
        conn.close()
        return SL
def Data_UP(Myj):
        con = MySQLdb.connect(
        host='',
        port = 3306,
        user='',
        passwd='',
        db ='',
        )
        cxr = con.cursor()
        cxr.execute(Myj)
        cxr.close()
        con.commit()
        con.close()
def MPM(slt):
	conn= MySQLdb.connect(
        host='',
        port = 3306,
        user='',
        passwd='',
        db ='',
        )
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        cur.execute("set names utf8;")
        sltresult=cur.execute(slt)
        CL = cur.fetchmany(sltresult)
        cur.close()
        conn.close()
        return CL
def lqjx_shut_game():
	ztsql = "update yw_game_operations set status = 2 where id = %s;" % Chann['id']
	Data_UP(ztsql)
        if int(Chann['isgroup']) == 2:
		SH1 = Chann['opservers']
		SH2 = re.findall("[0-9]{5}",SH1)
		for serid in SH2:
			hnSql = "select * from server where project_name = %s and name = %s ;" % (channel,serid)
			hostBH = json.loads(MPM(hnSql)[0]['extend'])['ex_gameserhost']
			SqlH = "select * from physics_server_pc where id = %s;" % hostBH
			HostN = MPM(SqlH)[0]['name']
			Spath = json.loads(MPM(hnSql)[0]['extend'])['ex_areapath']
			stop_ml = "salt \"%s\" cmd.run \'sh %sstop.sh\' > /tmp/stop_%s.log" %(HostN,Spath,serid)
			os.system(stop_ml)
			rzlog = "/tmp/stop_%s.log" % serid
			if os.path.isfile(rzlog):
				logf = open(rzlog)
				alllog = logf.read()
				logf.close()
				if "succ" in alllog or "Done" in alllog:
					IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'stop_game\',\'succ\',\'%s\');" % (Chann['id'],serid,serid,HostN)
					Data_UP(IRsql)
				else:
					IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'stop_game\',\'fail\',\'%s\');" % (Chann['id'],serid,serid,HostN)
					Data_UP(IRsql)
		zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
		Data_UP(zxsql)
	elif int(Chann['isgroup']) == 1:
		SH1 = Chann['opservers']
		SH2 = SH1.split(',')
		newsl = []
		for SHL in SH2:
			number = SHL.split('|')[0]
			newsl.append(number)
		for opserverl in newsl:
			OneSql = 'select s.name,s.extend from server s,server_group sg,servergroup_relation r where r.server_id=s.id and r.server_group_id=sg.id and sg.name=\"%s\" and sg.project_name=%s;' %(opserverl,channel)
			for serverL in MPM(OneSql):
				game_id = json.loads(serverL['name'])
				hostBH = json.loads(serverL['extend'])['ex_gameserhost']
				Spath = json.loads(serverL['extend'])['ex_areapath']
				SqlH = "select * from physics_server_pc where id = %s;" % hostBH
				HostN = MPM(SqlH)[0]['name']
				stop_ml = "salt \"%s\" cmd.run \'sh %sstop.sh\' > /tmp/stop_%s.log" %(HostN,Spath,game_id)
				os.system(stop_ml)
				rzlog = "/tmp/stop_%s.log" % game_id
				if os.path.isfile(rzlog):
					logf = open(rzlog)
					alllog = logf.read()
					logf.close()
					if "succ" in alllog or "Done" in alllog:
						IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'stop_game\',\'succ\',\'%s\');" % (Chann['id'],opserverl,game_id,HostN)
						Data_UP(IRsql)
					else:
						IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'stop_game\',\'fail\',\'%s\');" % (Chann['id'],opserverl,game_id,HostN)
						Data_UP(IRsql)
		zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
		Data_UP(zxsql)
	else:
		print "Can not identify parameters;"
def lqjx_start_game():
        ztsql = "update yw_game_operations set status = 2 where id = %s;" % Chann['id']
        Data_UP(ztsql)
        if int(Chann['isgroup']) == 2:
                SH1 = Chann['opservers']
                SH2 = re.findall("[0-9]{5}",SH1)
                for serid in SH2:
                        hnSql = "select * from server where project_name = %s and name = %s ;" % (channel,serid)
                        hostBH = json.loads(MPM(hnSql)[0]['extend'])['ex_gameserhost']
                        SqlH = "select * from physics_server_pc where id = %s;" % hostBH
                        HostN = MPM(SqlH)[0]['name']
                        Spath = json.loads(MPM(hnSql)[0]['extend'])['ex_areapath']
                        start_ml = "salt \"%s\" cmd.run \'sh %sstart.sh\' > /tmp/start_%s.log" %(HostN,Spath,serid)
                        os.system(start_ml)
                        rzlog = "/tmp/start_%s.log" % serid
                        if os.path.isfile(rzlog):
                                logf = open(rzlog)
                                alllog = logf.read()
                                logf.close()
                                if "succ" in alllog or "Done" in alllog:
                                        IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'start_game\',\'succ\',\'%s\');" % (Chann['id'],serid,serid,HostN)
                                        Data_UP(IRsql)
                                else:
                                        IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'start_game\',\'fail\',\'%s\');" % (Chann['id'],serid,serid,HostN)
                                        Data_UP(IRsql)
                zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
                Data_UP(zxsql)
        elif int(Chann['isgroup']) == 1:
                SH1 = Chann['opservers']
                SH2 = SH1.split(',')
                newsl = []
                for SHL in SH2:
                        number = SHL.split('|')[0]
                        newsl.append(number)
                for opserverl in newsl:
			OneSql = 'select s.name,s.extend from server s,server_group sg,servergroup_relation r where r.server_id=s.id and r.server_group_id=sg.id and sg.name=\"%s\" and sg.project_name=%s;' %(opserverl,channel)
			for serverL in  MPM(OneSql):
				game_id = json.loads(serverL['name'])
                                hostBH = json.loads(serverL['extend'])['ex_gameserhost']
                                Spath = json.loads(serverL['extend'])['ex_areapath']
                                SqlH = "select * from physics_server_pc where id = %s;" % hostBH
                                HostN = MPM(SqlH)[0]['name']
                                start_ml = "salt \"%s\" cmd.run \'sh %sstart.sh\' > /tmp/start_%s.log" %(HostN,Spath,game_id)
                                os.system(start_ml)
                                rzlog = "/tmp/start_%s.log" % game_id
                                if os.path.isfile(rzlog):
                                        logf = open(rzlog)
                                        alllog = logf.read()
                                        logf.close()
                                        if "succ" in alllog or "Done" in alllog:
                                                IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'start_game\',\'succ\',\'%s\');" % (Chann['id'],opserverl,game_id,HostN)
                                                Data_UP(IRsql)
                                        else:
                                                IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'start_game\',\'fail\',\'%s\');" % (Chann['id'],opserverl,game_id,HostN)
                                                Data_UP(IRsql)
                zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
                Data_UP(zxsql)
	else:
		print "Can not identify parameters;"
def mysql_backup_lqjx():
        ztsql = "update yw_game_operations set status = 2 where id = %s;" % Chann['id']
        Data_UP(ztsql)
        if int(Chann['isgroup']) == 2:
                SH1 = Chann['opservers']
                SH2 = re.findall("[0-9]{5}",SH1)
                for serid in SH2:
			ljf = '_'
			bserid = str(serid)
			pj = 'lqjx',bserid
			myname = ljf.join(pj)
                        hnSql = "select * from server where project_name = %s and name = %s ;" % (channel,serid)
                        hostBH = json.loads(MPM(hnSql)[0]['extend'])['ex_gameserhost']
                        SqlH = "select * from physics_server_pc where id = %s;" % hostBH
                        HostN = MPM(SqlH)[0]['name']
			DBBH = json.loads(MPM(hnSql)[0]['extend'])['ex_dbserhost']
			SqlD = "select * from physics_server_pc where id = %s;" % DBBH
			DBN = MPM(SqlD)[0]['inner_ip']
                        back_ml = "salt \"lqjx-log\" cmd.run \'sh /alidata1/script/lqjx_mysql_backup.sh %s  %s\' > /tmp/mysql_back_%s.log" %(DBN,myname,serid)
                        os.system(back_ml)
                        rzlog = "/tmp/mysql_back_%s.log" % serid
                        if os.path.isfile(rzlog):
                                logf = open(rzlog)
                                alllog = logf.read()
                                logf.close()
                                if "succ" in alllog:
                                        IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'mysql_back\',\'succ\',\'%s\');" % (Chann['id'],serid,serid,HostN)
                                        Data_UP(IRsql)
                                else:
                                        IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'mysql_back\',\'fail\',\'%s\');" % (Chann['id'],serid,serid,HostN)
                                        Data_UP(IRsql)
                zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
                Data_UP(zxsql)
def lqjx_rsync_list():
        ztsql = "update yw_game_operations set status = 2 where id = %s;" % Chann['id']
        Data_UP(ztsql)
	rsync_ml = "salt \"app-web-01\" cmd.run \'sh /alidata1/vhosts/list.lqjx.youlongteng.com/production/rsync_lqjx_list.sh\' > /tmp/lqjx_rsync.log"
	os.system('rm -f /tmp/lqjx_rsync.log')
	os.system(rsync_ml)
	if os.path.isfile("/tmp/lqjx_rsync.log"):
		logf = open("/tmp/lqjx_rsync.log")
		alllog  = logf.read()
		logf.close()
		if "succ" in alllog:
			Rsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'all\',\'all\',\'rsync_list\',\'succ\',\'app-web-01\');" % Chann['id']
			Data_UP(Rsql)
		else:
			Rsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'all\',\'all\',\'rsync_list\',\'fail\',\'app-web-01\');" % Chann['id']
			Data_UP(Rsql)
	zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
	Data_UP(zxsql)
def lqjx_rsync_game():
        ztsql = "update yw_game_operations set status = 2 where id = %s;" % Chann['id']
        Data_UP(ztsql)
        if int(Chann['isgroup']) == 2:
                SH1 = Chann['opservers']
                SH2 = re.findall("[0-9]{5}",SH1)
                for serid in SH2:
                        hnSql = "select * from server where project_name = %s and name = %s ;" % (channel,serid)
                        hostBH = json.loads(MPM(hnSql)[0]['extend'])['ex_gameserhost']
                        SqlH = "select * from physics_server_pc where id = %s;" % hostBH
                        HostN = MPM(SqlH)[0]['name']
                        Spath = json.loads(MPM(hnSql)[0]['extend'])['ex_areapath']
                        rsync_ml = "salt \"%s\" cmd.run \'sh /alidata1/scripts/rsync_lqjx.sh  %s\' > /tmp/rsync_%s.log" %(HostN,Spath,serid)
                        os.system(rsync_ml)
                        rzlog = "/tmp/rsync_%s.log" % serid
                        if os.path.isfile(rzlog):
                                logf = open(rzlog)
                                alllog = logf.read()
                                logf.close()
                                if "succ" in alllog:
                                        IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'rsync_game\',\'succ\',\'%s\');" % (Chann['id'],serid,serid,HostN)
                                        Data_UP(IRsql)
                                else:
                                        IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'rsync_game\',\'fail\',\'%s\');" % (Chann['id'],serid,serid,HostN)
                                        Data_UP(IRsql)
                zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
                Data_UP(zxsql)
        elif int(Chann['isgroup']) == 1:
                SH1 = Chann['opservers']
                SH2 = SH1.split(',')
                newsl = []
                for SHL in SH2:
                        number = SHL.split('|')[0]
                        newsl.append(number)
                for opserverl in newsl:
			OneSql = 'select s.name,s.extend from server s,server_group sg,servergroup_relation r where r.server_id=s.id and r.server_group_id=sg.id and sg.name=\"%s\" and sg.project_name=%s;' %(opserverl,channel)
                        for serverL in MPM(OneSql):
                                game_id = json.loads(serverL['name'])
                                hostBH = json.loads(serverL['extend'])['ex_gameserhost']
                                Spath = json.loads(serverL['extend'])['ex_areapath']
                                SqlH = "select * from physics_server_pc where id = %s;" % hostBH
                                HostN = MPM(SqlH)[0]['name']
                                rsync_ml = "salt \"%s\" cmd.run \'sh /alidata1/scripts/rsync_lqjx.sh  %s\' > /tmp/rsync_%s.log" %(HostN,Spath,game_id)
                                os.system(rsync_ml)
                                rzlog = "/tmp/rsync_%s.log" % game_id
                                if os.path.isfile(rzlog):
                                        logf = open(rzlog)
                                        alllog = logf.read()
                                        logf.close()
                                        if "succ" in alllog or "Done" in alllog:
                                                IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'rsync_game\',\'succ\',\'%s\');" % (Chann['id'],opserverl,game_id,HostN)
                                                Data_UP(IRsql)
                                        else:
                                                IRsql = "insert into yw_result_operations(game_opid,sergrop,serid,contents,status,memo) values(\'%s\',\'%s\',\'%s\',\'rsync_game\',\'fail\',\'%s\');" % (Chann['id'],opserverl,game_id,HostN)
                                                Data_UP(IRsql)
                zxsql = "update yw_game_operations set status = 3 where id = %s;" % Chann['id']
                Data_UP(zxsql)
        else:
                print "Can not identify parameters;"
def setup():
	global Chann
	global channel
        cstatus = mysql_ML("select * from yw_game_operations where status = 1 and isrew = 1;")
        if len(cstatus) > 0:
                for Pl in range(len(cstatus)):
			Chann =  cstatus[Pl]
                        channel = int(Chann['game_id'])
                        if channel == 1023:
                                content = int(Chann['optype'])
				ISOTIMEFORMAT='%Y-%m-%d %X'
				now_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
				exec_time = Chann['operationtime']
				print "exec_time",exec_time
				print "now_time",now_time
				if str(now_time) >= str(exec_time):
					if content == 2:
						lqjx_shut_game()
					elif content == 1:
						lqjx_rsync_list()
					elif content == 5:
						lqjx_start_game()
					elif content == 3:
						mysql_backup_lqjx()
					elif content == 4:
						lqjx_rsync_game()
					else:
						print "Without the opening of the function, please contact the system administrator!"
				else:
					print "Did not reach the execution time, attention please!"
                        elif channel == "axl":
				pass
                        else:
                                print "Game project is not add operation system platform, please contact your administrator!"
if __name__ == '__main__':
	while True:
        	setup()
		time.sleep(60)
