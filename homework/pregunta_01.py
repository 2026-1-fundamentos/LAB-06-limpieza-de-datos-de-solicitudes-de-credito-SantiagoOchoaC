"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import os
    import pandas as pd


    def load_data(input_path):
        return pd.read_csv(input_path, sep=";", index_col=0)

    def normalizar(df, columns):
        for col in columns:
            df[col] = df[col].str.lower().str.strip()
        return df

    def normalizar_separadores(df, columns):
        for col in columns:
            df[col] = (
                df[col].str.replace("-", " ").str.replace("_", " ").str.split().str.join(" "))
        return df

    def limpiar_monto_del_credito(df):
        df["monto_del_credito"] = (
            df["monto_del_credito"]
            .str.replace("$", "")
            .str.replace(",", "")
            .str.replace(" ", "")
            .str.removesuffix(".00")
            .str.replace(".", "")
            .astype(float)
            .astype(int)
        )
        return df

    def limpiar_fecha_beneficio(df):
        fecha_dia_mes = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
        fecha_anio_mes = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
        df["fecha_de_beneficio"] = fecha_dia_mes.fillna(fecha_anio_mes)
        return df

    def clean_data(df):
        df = df.dropna()

        df = normalizar(df, ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"])
        df = normalizar_separadores(df, ["idea_negocio", "línea_credito"])

        df["barrio"] = (df["barrio"].str.lower().str.replace("-", " ").str.replace("_", " "))

        df = limpiar_monto_del_credito(df)
        df = limpiar_fecha_beneficio(df)

        df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
        df = df.drop_duplicates()

        return df


    def save_data(df, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, sep=";", index=False)


    def main(input_file, output_file):
        df = load_data(input_file)
        df = clean_data(df)
        save_data(df, output_file)

    if __name__ == "__main__":
        main("files/input/solicitudes_de_credito.csv", "files/output/solicitudes_de_credito.csv")
