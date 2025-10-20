import pyodbc


def absortion_column_publish(driver, server, database, UID, PWD, HE, HETP, Xn, ns):

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
                
    try:    
        insert_query ="INSERT INTO [dbo].[equimpent_absortion_column] ([HE],[HETP],[Xn],[ns]) VALUES (?,?,?,?)"
        cursor.execute(insert_query,str(HE),str(HETP),str(Xn),str(ns))       
    except:
        cnxn.rollback()
    finally:
        cnxn.commit()
        cnxn.close()


def compressor_publish(driver, server, database, UID, PWD, m, W_total, P_real):
    
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    
    try:    
        insert_query ="INSERT INTO [dbo].[equimpent_compressor] ([m],[W_total],[P_real]) VALUES (?,?,?)"
        cursor.execute(insert_query,str(m),str(W_total),str(P_real))       
    except:
        cnxn.rollback()
    finally:
        cnxn.commit()
        cnxn.close()

def distillator_column_publish(driver, server, database, UID, PWD,N2_out,O2_out,Ar_out):
    
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    try:    
        insert_query ="INSERT INTO [dbo].[equimpent_distillaor_column] ([N2_out],[O2_out],[Ar_out]) VALUES (?,?,?)"
        cursor.execute(insert_query,str(N2_out),str(O2_out),str(Ar_out))       
    except:
        cnxn.rollback()
    finally:
        cnxn.commit()
        cnxn.close()    

def heat_exchanger_publish(driver, server, database, UID, PWD,):

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    try:    
        insert_query ="INSERT INTO [dbo].[heat_exchanger] ([Q_air],[Q_nitrogen],[delta_T_ml],[m_cooling],[A_tubes],[v_air],[reynolds_air],[f_air],[delta_P_air],[delta_P_nitrogen],[v_nitrogen],[reynolds_nitrogen],[f_nitrogen],[delta_nitrogen]) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(insert_query,str(result[0]),str(result[1]),str(result[2]),str(result[3]),result[4],str(result[5]),str(result[6]),str(result[7]),result[8],str(result[9]),str(result[10]),str(result[11]),str(result[12]),str(result[13]))       
    except:
        cnxn.rollback()
    finally:
        cnxn.commit()
        cnxn.close()

def valve_joule_thompson_publish():

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    try:    
        insert_query ="INSERT INTO [dbo].[xxxx] ([P_out],[T_in],[T_out]) VALUES (?,?,?)"
        cursor.execute(insert_query,str(result[0]),str(result[1]),str(result[2]))       
    except:
        cnxn.rollback()
    finally:
        cnxn.commit()
        cnxn.close()
