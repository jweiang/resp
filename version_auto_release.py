# -*- coding: utf-8 -*-
#!/usr/bin/env python
#link---joy
#version 1.0 2015-08-26

#import time
import os
import MySQLdb
 
def mysql_ML(slt):
	conn= MySQLdb.connect(
	host='',
	port = 3306,
	user='',
	passwd='',
	db ='',
	)
	cur = conn.cursor()
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
def Sharing():
	global prereleaseurl
	global onlineurl
	global prereleasedir
	global onlinedir
	global pre_name
	Psql = "select id,prereleaseurl,onlineurl,name,prereleasedir,onlinedir from yw_project_releases where id = %s" % proj_res_id
	FB = mysql_ML(Psql)
	prereleaseurl = FB[0][1]
	onlineurl = FB[0][2]
	prereleasedir = FB[0][4] 
	onlinedir = FB[0][5]
	pre_name = FB[0][3]
def Pre_release():
	pre_path = "/alidata1/code_publish/%s" % pre_name 
	os.chdir(pre_path)
	os.system('svn up')
	os.system('git add .')
	Gt = 'git commit -m \"update version %s\"' % VerSion
	os.system(Gt)
	os.system('rm -f /tmp/version.log')
	RShell = "salt \'%s\' cmd.run \'sh /alidata1/scripts/wswtest.sh %s  %s\' > /tmp/version.log" % (prereleaseurl,pre_name,prereleasedir)
	os.system(RShell)
	if os.path.isfile("/tmp/version.log"):
		logf = open("/tmp/version.log")
		alllog  = logf.read()
		logf.close()
		if "succ" in alllog:
			sql = "update yw_released_versions set status = 2 where id = %s" % IDV
			Data_UP(sql)
		else:
			sql = "update yw_released_versions set status = 901 where id = %s" % IDV
			Data_UP(sql)
	else:
		print "Pre_release  Did not generate log"
def Release():
	pre_path = "/alidata1/code_publish/%s" % pre_name
	os.chdir(pre_path)
	os.system('rm -f /tmp/version.log')
	RShell = "salt \'%s\' cmd.run \'sh /alidata1/scripts/wswtest.sh %s %s\' > /tmp/version.log" % (onlineurl,pre_name,onlinedir)
	os.system(RShell)
        if os.path.isfile("/tmp/version.log"):
		logf = open("/tmp/version.log")
		alllog  = logf.read()
                logf.close()
                if "succ" in alllog:
                        sql = "update yw_released_versions set status = 6 where id = %s" % IDV
                        Data_UP(sql)
			branch_v = "git branch %s" % VerSion
			os.system(branch_v)
                else:
                        sql = "update yw_released_versions set status = 905 where id = %s" % IDV
                        Data_UP(sql)
        else:
                print "Release Did not generate log"
def Retreated():
	pre_path = "/alidata1/code_publish/%s" % pre_name
	os.chdir(pre_path)
	hversion = int(VerSion)
	HD_version = hversion - 1
	GH = "git checkout %s" % HD_version
	os.system(GH)
	os.system('rm -f /tmp/version.log')
	RShell = "salt \'%s\' cmd.run \'sh /alidata1/scripts/wswtest.sh %s %s\' > /tmp/version.log" % (onlineurl,pre_name,onlinedir)
	os.system(RShell)
        if os.path.isfile("/tmp/version.log"):
		logf = open("/tmp/version.log")
                alllog  = logf.read()
                logf.close()
                if "succ" in alllog:
                        sql = "update yw_released_versions set status = 10 where id = %s" % IDV
			Data_UP(sql)
			os.system("git checkout master")
                else:
                        sql = "update yw_released_versions set status = 908 where id = %s" % IDV
                        Data_UP(sql)
        else:
                print "Retreated Did not generate log"
def setup():
	global IDV
	global VerSion
	global proj_res_id
	mstate = mysql_ML("select id,proj_res_id,res_version,status from yw_released_versions where status = 1;")
	if len(mstate) != 0:
		state = mstate[0][3]
		IDV = mstate[0][0]
		VerSion = mstate[0][2]
		proj_res_id = mstate[0][1]
		Sharing()
		if state == 1:
			Pre_release()
	mstate5 = mysql_ML("select id,proj_res_id,res_version,status from yw_released_versions  where status = 5;")
	if len(mstate5) != 0:
		state5 = mstate5[0][3]
		IDV = mstate5[0][0]
		VerSion = mstate5[0][2]
		proj_res_id = mstate5[0][1]
		Sharing()
		if state5 == 5:
			Release()
        mstate9 = mysql_ML("select id,proj_res_id,res_version,status from yw_released_versions  where status = 9;")
	if len(mstate9) != 0:
        	state9 = mstate9[0][3]
		IDV = mstate9[0][0]
		VerSion = mstate9[0][2]
		proj_res_id = mstate9[0][1]
		Sharing()
        	if state9 == 9:
                	Retreated()
if __name__ == '__main__':
	#while True:
	setup()
	#	time.sleep(60)

