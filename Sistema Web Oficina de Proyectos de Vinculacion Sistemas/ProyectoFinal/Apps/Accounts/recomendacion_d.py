import pandas as pd
import numpy as np

# Funcion para limpiar y organizar los datos


def matrix_anteproyectos_materias(df_anteproyectos, df_anteproyecto_materia, df_materias):
    # Se eliminan aquellos atributos que no son necesarios y se renombra una columna para hacer la union con otro dataframe
    df_anteproyectos = df_anteproyectos.drop(['revisor1_id', 'revisor2_id', 'dependencia_id', 'asesorExterno_id', 'observacion_id', 'anteproyectoDoc', 'codigoUnion', 'fechaEntrega', 'numIntegrantes'], axis=1)
    df_anteproyectos.rename(columns = {'id':'anteproyecto_id'}, inplace = True)
    df_materias.rename(columns = {'id':'materia_id'}, inplace = True)
    
    # Union de anteproyecto con materia
    df_anteproyecto_materia_union = pd.merge(df_anteproyecto_materia, df_materias, on="materia_id")
    df_anteproyecto_materia_union = df_anteproyecto_materia_union.drop(['materia_id', 'nombre', 'semestre', 'id'], axis=1)
    
    # Se agrupan las materias por anteproyecto
    df_grouped = df_anteproyecto_materia_union.groupby(df_anteproyecto_materia_union.anteproyecto_id)
    
    # Se crea la matriz principal
    columns_series = df_materias['clave']
    columns_list = columns_series.tolist()
    columns_list.insert(0, 'anteproyecto_id')
    df_matrix_anteproyecto_materias = pd.DataFrame(columns=columns_list)
    
    # Se agrega cada anteproyecto con sus respectivas materias a la matriz
    for k, g in df_grouped:    
        list_keys = df_grouped.get_group(k)['clave']
        list_keys = list_keys.tolist()
        list_values = df_grouped.get_group(k)['compatibilidad']
        list_values = list_values.tolist()    
        dictionary_materias = {list_keys[i]: list_values[i] for i in range(len(list_keys))}    
        dictionary_materias['anteproyecto_id'] = k      
        df_dictionary = pd.DataFrame(dictionary_materias, index=[0])    
        df_matrix_anteproyecto_materias = df_matrix_anteproyecto_materias.append(df_dictionary, ignore_index = True)
    
    
    return df_matrix_anteproyecto_materias  

# Funcion que recibe un df de las materias, un df de los docentes y un df de 
# los perfiles academicos de cada docente
def matrix_docentes_materias(df_materias, df_docentes, df_perfil_academico):
    df_docentes = df_docentes[['id', 'perfilAcademico_id', 'nombre']]
    df_materias.rename(columns = {'id':'materia_id'}, inplace = True)
    columns_series = df_materias['clave']
    columns_list = columns_series.tolist()
    columns_list.insert(0, 'perfilAcademico_id')
    df_matrix_docentes_materias = pd.DataFrame(columns=columns_list)
    
    df_perfil_meteria_union = pd.merge(df_perfil_academico, df_materias, on="materia_id")
    df_perfil_meteria_union = df_perfil_meteria_union.drop(['materia_id'], axis=1)
    df_grouped = df_perfil_meteria_union.groupby(df_perfil_meteria_union.perfilacademico_id)
    
    for k, g in df_grouped:    
        list_keys = df_grouped.get_group(k)['clave']
        list_keys = list_keys.tolist()
        dictionary_keys = dict.fromkeys(list_keys, 10)    
        dictionary_keys['perfilAcademico_id'] = k  
        df_dictionary = pd.DataFrame(dictionary_keys, index=[0])
        df_matrix_docentes_materias = df_matrix_docentes_materias.append(df_dictionary, ignore_index = True)
    
    df_matrix_docentes_materias = pd.merge(df_docentes, df_matrix_docentes_materias, on='perfilAcademico_id')
    df_matrix_docentes_materias = df_matrix_docentes_materias.drop(['perfilAcademico_id'], axis=1)
    df_matrix_docentes_materias.rename(columns = {'id':'docente_id'}, inplace = True)
    
    return df_matrix_docentes_materias 

# Creacion del modelo


def similitud_coseno(anteproyecto_punt, docente_punt):
    # Se calcula el producto escalar
    dot_product = np.dot(anteproyecto_punt, docente_punt)
    # Se calcula la distancia euclidea
    norm_anteproyecto = np.linalg.norm(anteproyecto_punt)
    # Se calcula la segunda distancia euclidea
    norm_docente = np.linalg.norm(docente_punt)
    return dot_product / (norm_anteproyecto * norm_docente)

def recomendacion_docentes(anteproyectos_df, docentes_df, anteproyecto_id, n):    
    # Seleccionar fila de usuario de anteproyectos_df
    anteproyecto_punt = anteproyectos_df[anteproyectos_df['anteproyecto_id'] == anteproyecto_id].drop(columns=['anteproyecto_id']).values[0]
    
    # Se crea un nuevo dataframe para almacenar los puntajes de similitud de coseno para cada par usuario-docente
    punt_df = pd.DataFrame(columns=['anteproyecto_id', 'docente_id', 'similitud_coseno_punt'])
    
    # Se itera sobre cada docente en docentes_df
    for i, docente in docentes_df.iterrows():
        # Se obtienen los valores del docente
        #docente_punt = docente.drop(columns=['docente_id']).values
        docente_punt = docente.drop('docente_id').values        
        # Se calcula la similitud de coseno entre el anteproyecto y el docente
        similitud_coseno_punt = similitud_coseno(anteproyecto_punt, docente_punt)
                
        # Se guarda el coseno de similitud del anteproyecto y docente
        punt_df = punt_df.append({
            'anteproyecto_id': anteproyecto_id,
            'docente_id': docente['docente_id'],
            'similitud_coseno_punt': similitud_coseno_punt
        }, ignore_index=True)
        
    # Se ordenan los resultados del coseno de similitud, de mayor a menor.
    punt_df = punt_df.sort_values(by='similitud_coseno_punt',ascending=False)
    # Se obtienen los docentes recomendados
    top_docentes = punt_df.head(n)
    # Se convierte el dataframe a una lista con el id de cada docente
    docentes_list = top_docentes['docente_id'].tolist()
    return docentes_list



# Funcion principal

def recomendaciones_docentes(df_anteproyectos, df_anteproyecto_materia, df_docentes, df_perfil_academico, df_materias, num_docentes = 3):
    mx_docentes = matrix_docentes_materias(df_materias, df_docentes, df_perfil_academico)
    mx_anteproyectos = matrix_anteproyectos_materias(df_anteproyectos, df_anteproyecto_materia, df_materias)
    mx_docentes = mx_docentes.drop('nombre', axis=1)
    df_doc = mx_docentes.replace(np.nan, 0)
    df_ant = mx_anteproyectos.replace(np.nan, 0)
    anteproyecto_pk = df_ant.iloc[0, 0]
    recomendaciones = recomendacion_docentes(df_ant, df_doc, anteproyecto_pk, num_docentes)    
    return recomendaciones


