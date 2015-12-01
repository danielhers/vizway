#!/usr/bin/python
import psycopg2
import os

from glob import glob


if __name__ == "__main__":
    conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (
            os.getenv("PSQL_HOST"), os.getenv("PSQL_DB"),
            os.getenv("PSQL_USER"), os.getenv("PSQL_PASSWORD"))
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE acc_data (pk_teuna_fikt integer,sug_tik integer,THUM_GEOGRAFI integer,SUG_DEREH integer,SEMEL_YISHUV integer,REHOV1 integer,REHOV2 integer,BAYIT integer,ZOMET_IRONI integer,KVISH1 integer,KVISH2 integer,KM integer,ZOMET_LO_IRONI integer,YEHIDA integer,SHNAT_TEUNA integer,HODESH_TEUNA integer,YOM_BE_HODESH integer,SHAA integer,SUG_YOM integer,YOM_LAYLA integer,YOM_BASHAVUA integer,RAMZOR integer,HUMRAT_TEUNA integer,SUG_TEUNA integer,ZURAT_DEREH integer,HAD_MASLUL integer,RAV_MASLUL integer,MEHIRUT_MUTERET integer,TKINUT integer,ROHAV integer,SIMUN_TIMRUR integer,TEURA integer,BAKARA integer,MEZEG_AVIR integer,PNE_KVISH integer,SUG_EZEM integer,MERHAK_EZEM integer,LO_HAZA integer,OFEN_HAZIYA integer,MEKOM_HAZIYA integer,KIVUN_HAZIYA integer,MAHOZ integer,NAFA integer,EZOR_TIVI integer,MAAMAD_MINIZIPALI integer,ZURAT_ISHUV integer,STATUS_IGUN integer,X integer,Y integer);")

    for filename in glob("static/data/lms/Accidents Type */*/*AccData.csv"):
        print "Importing '%s'... " % filename
        with open(filename) as f:
            f.readline()
            cursor.copy_from(f, "acc_data", sep=",", null="")

    cursor.execute("CREATE TABLE inv_data (pk_teuna_fikt integer,MISPAR_REHEV_fikt integer,ZEHUT_fikt integer,SHNAT_TEUNA integer,HODESH_TEUNA integer,SUG_MEORAV integer,SHNAT_HOZAA integer,KVUZA_GIL integer,MIN integer,SUG_REHEV_NASA_LMS integer,EMZAE_BETIHUT integer,SEMEL_YISHUV_MEGURIM integer,HUMRAT_PGIA integer,SUG_NIFGA_LMS integer,PEULAT_NIFGA_LMS integer,KVUTZAT_OHLUSIYA_LMS integer,MAHOZ_MEGURIM integer,NAFA_MEGURIM integer,EZOR_TIVI_MEGURIM integer,MAAMAD_MINIZIPALI_MEGURIM integer,ZURAT_ISHUV_MEGURIM integer,SUG_TIK integer,PazuaUshpaz_LMS integer,ISS_LMS integer,YaadShihrur_PUF_LMS integer,ShimushBeAvizareyBetihut_LMS integer,PtiraMeuheret_LMS integer);")

    for filename in glob("static/data/lms/Accidents Type */*/*InvData.csv"):
        print "Importing '%s'... " % filename
        with open(filename) as f:
            f.readline()
            cursor.copy_from(f, "inv_data", sep=",", null="")

    conn.commit()
    conn.close()

    print "Import complete."
