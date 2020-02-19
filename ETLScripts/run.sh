#! /bin/sh

cd ./
#--========数据分析========================================================================--
#加载ASS层脚本
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_CLS_OWN_CLASS_INFO_CUR.HQL   2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_CLS_SCHEDULE_D.HQL           2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_CLS_TEACH_CLASS_INFO_CUR.HQL 2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_CLASS_EVALUATE_D.HQL     2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_PAPER_INFO_CUR.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_PAPER_PUBLISH_D.HQL      2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_PAPER_RESULT_D.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_PAPER_STATUS_D.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_QUESTION_INFO_CUR.HQL    2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_QUSN_KNWG_REL_CUR.HQL    2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVT_AISCH_ACTION_LOG_D.HQL   2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVT_TASK_CREATE_D.HQL        2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVT_TASK_PUBLISH_D.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVT_TASK_RESULT_D.HQL        2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_RES_DEVICE_CUR.HQL           2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_RES_DEVICE_USAGE_D.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_RES_RESOURCE_INFO_CUR.HQL    2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_RES_RESOURCE_USAGE_D.HQL     2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_SCH_BASIC_INFO_CUR.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_SCH_CLIENT_VERSION_CUR.HQL   2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_SCH_TERM_INFO_D.HQL          2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_STD_BASIC_INFO_CUR.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_STD_KNOWLEDGE_CUR.HQL        2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_STD_STATUS_INFO_CUR.HQL      2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_STD_TEACH_CLS_CUR.HQL        2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_TCH_BASIC_INFO_CUR.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_TCH_GRADE_REL_CUR.HQL        2018-10-14 120102 0 &&

python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_STD_HEALTH_MAP_Y.HQL         2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_STD_HEALTH_DTL_Y.HQL         2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_STD_HEALTH_RPT_Y.HQL         2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVL_KNOWLEDGE_INFO_CUR.HQL   2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/01_ass/ASS_EVT_USER_ACTION_D.HQL        2018-10-14 120102 0 &&

#加载DIM层脚本
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/08_dim/DIM_ORG_CLS.HQL  2018-10-14 120102 0 &&

#加载LAB层脚本
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_EVL_KNOWLEDGE_TYPE_D.HQL  2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_STD_NEW_STUDENT_D.HQL     2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_TCH_COURSE_TEACHER_D.HQL  2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_TCH_NEW_TEACHER_D.HQL     2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_STD_KNOWLEDGE_D.HQL       2018-10-14 120102 0 &&

#加载BAS层脚本
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/03_bas/BAS_STD_BASIC_INFO_D.HQL  2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/03_bas/BAS_TCH_BASIC_INFO_D.HQL  2018-10-14 120102 0 &&

#加载APP层脚本
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_INFO_DTL_D.HQL          2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TCH_INFO_DTL_D.HQL          2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_HEALTH_SUM_D.HQL        2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_KNOWLEDGE_DTL_D.HQL     2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_STATISTICS_SUM_D.HQL    2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TCH_STATISTICS_SUM_D.HQL    2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TEACH_SUBJECT_SUM_D.HQL     2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TEACH_TASKS_SUM_D.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TEACH_TEACHER_SUM_D.HQL     2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TEACH_TOOLS_SUM_D.HQL       2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TERMINAL_USE_SUM_D.HQL      2018-10-14 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TOTAL_STATISTICS_SUM_D.HQL  2018-10-14 120102 0 &&


#--========综合评价========================================================================--
#加载LAB层脚本
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_STD_EVL_ITEM_VAL_M.HQL        2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_TCH_EVL_ITEM_VAL_M.HQL        2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/INIT_LAB_STD_EVL_ITEM_SCORE_M.HQL 2018-XX 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/INIT_LAB_TCH_EVL_ITEM_SCORE_M.HQL 2018-XX 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_STD_EVL_ITEM_SCORE_M.HQL      2018-XX 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_TCH_EVL_ITEM_SCORE_M.HQL      2018-XX 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_STD_EVL_K1_M.HQL              2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/02_lab/LAB_TCH_EVL_K2_M.HQL              2018-11 120102 0 &&

#加载APP层脚本
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1001001_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1001002_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1001_M.HQL    2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1002001_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1002002_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1002003_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1002004_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1002005_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1002_M.HQL    2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1003001_M.HQL 2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1003_M.HQL    2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1004_M.HQL    2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1005_M.HQL    2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1_M.HQL       2018-11 120102 0 &&

python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1_LVL_M.HQL   2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_STD_EVL_K1_NOTE_M.HQL  2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TCH_EVL_K2_M.HQL       2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TCH_EVL_K2_LVL_M.HQL   2018-11 120102 0 &&
python ./SQLJobParser/JOBParser/JobParser.py ./SQLScripts/05_app/REP_TCH_EVL_K2_NOTE_M.HQL  2018-11 120102 0 &&
