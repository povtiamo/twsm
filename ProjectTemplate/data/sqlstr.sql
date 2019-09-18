
SELECT userid FROM t_e_user_logininfo where loginname='examTm001' limit 1;

SELECT userid FROM t_e_user_logininfo where loginname='jyjls01' limit 1;

SELECT * FROM t_e_teacher WHERE name LIKE 'examT1%';
SELECT * FROM t_e_student WHERE name LIKE '%s_bat221613%';
SELECT * FROM t_e_student WHERE name LIKE '%s_bat221613_1%1%1%';
#SELECT * FROM t_e_user_logininfo WHERE loginname LIKE '%examT_%' AND status != '7';

#SELECT * FROM t_con_role_org_edu;
#SELECT * FROM t_e_sys_role where rolename='云考试默认教师角色';
#SELECT * from	 t_con_user_role WHERE createtime>='2019-07-31 10:15:47.900098';
#SELECT * FROM t_e_teacher where id in(SELECT userid from t_con_user_role);
#select count(*) from pg_stat_activity;
#select * from pg_stat_activity;

#SELECT * FROM t_e_teacher WHERE  name NOT like'examT_3110%' and name LIKE 'examT%';
#SELECT * from t_con_class_subject WHERE classid in(
#SELECT classid from t_e_class WHERE classname LIKE 'class3110_1%');

#SELECT
	t1.loginname,
	t2.roleid,
	t3.rolename
FROM
	t_e_user_logininfo t1
INNER JOIN t_con_user_role t2
ON t1.userid = t2.userid
INNER JOIN t_e_sys_role t3 
ON t2.roleid = t3.roleid;
