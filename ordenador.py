import pandas as pd

def ordenar_datos(input, out_path):
    a = pd.read_json(input)
    columnas = {
        'experience': ["nombre_puesto", "empleador", "permanencia", "ubicacion", "url"],
        'volunteering_experience':['titulo', 'lugar', 'plazo', 'categoria'],
        'education':['nombre','lugar','plazo','url'],
        'languages':['idioma', 'nivel'],
    }

    dfs = {
        'experience': pd.DataFrame(columns=["perfil", "error"]+columnas['experience']),
        'volunteering_experience':pd.DataFrame(columns=["perfil", "error"]+columnas['volunteering_experience']),
        'education':pd.DataFrame(columns=["perfil", "error"]+columnas['education']),
        'languages':pd.DataFrame(columns=["perfil", "error"]+columnas['languages'])
    }

    for index, row in a.iterrows():
        for cat in list(columnas.keys()):
            for dato in row[cat]:
                aux = dato
                if type(aux) == str:
                    continue
                aux["perfil"] = row["url"]
                dfs[cat] = dfs[cat].append(aux,ignore_index=True)

    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        for cat in list(columnas.keys()):
            dfs[cat].to_excel(writer, sheet_name=cat, index=False)
        a.to_excel(writer, sheet_name='general', index=False)
