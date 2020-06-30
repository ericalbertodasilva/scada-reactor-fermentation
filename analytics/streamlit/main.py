import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def main():
    st.title("Analisador de dados de fermentação")
    st.subheader("Antes de utilizar aplicação é necessario ter os arquivos .csv diponibilizado pelo reator Minifors 2 e medidor de CO2")

    physical_chemical_analysis = st.file_uploader("Por favor escolher arquivo como analises fisico-quimicas '*.csv'", type='csv')
    if physical_chemical_analysis is not None:
        df_physical_chemical_analysis = pd.read_csv(physical_chemical_analysis,
                                                    sep=';')
        df_physical_chemical_analysis.loc[:, 'Tempo (h)'] = pd.to_datetime(df_physical_chemical_analysis['Tempo (h)'],
                                                                           format="%Y-%m-%d %H:%M:%S")
        df_physical_chemical_analysis['Viabilidade'] = df_physical_chemical_analysis['Viabilidade']\
            .str.replace(",", ".").astype(float)
        df_physical_chemical_analysis['BRIX'] = df_physical_chemical_analysis['BRIX']\
            .str.replace(",", ".").astype(float)
        df_physical_chemical_analysis['ART (g/L)'] = df_physical_chemical_analysis['ART (g/L)']\
            .str.replace(",", ".").astype(float)
        df_physical_chemical_analysis['Glicerol (g/L)'] = df_physical_chemical_analysis['Glicerol (g/L)']\
            .str.replace(",", ".").astype(float)
        df_physical_chemical_analysis['Biomassa (g/L)'] = df_physical_chemical_analysis['Biomassa (g/L)']\
            .str.replace(",", ".").astype(float)
        df_physical_chemical_analysis['Teor Alcoolico (v/v)'] = df_physical_chemical_analysis['Teor Alcoolico (v/v)']\
            .str.replace(",", ".").astype(float)
        st.markdown("Tabela de analises fisico-quimicas")
        st.dataframe(df_physical_chemical_analysis)

        infors_reactor_measurements = st.file_uploader(
            "Por favor escolher arquivo exportado do reator Minifors 2 com final '*Measurements.csv'",
            type='csv')
        if (infors_reactor_measurements is not None):
            df_infors_reactor_measurements = pd.read_csv(infors_reactor_measurements, sep=';')
            df_infors_reactor_measurements = df_infors_reactor_measurements.drop(
                ['ProcessTime', 'AF', 'Flow', 'GMFlow', 'Gas2Flow', 'GasMix', 'Pump1', 'Pump2', 'Pump3', 'Pump4',
                 'aio1', 'aio2'], axis=1)
            filter = ~df_infors_reactor_measurements.DateTime.isnull()
            df_infors_reactor_measurements = df_infors_reactor_measurements[filter]
            df_infors_reactor_measurements['Stirrer'] = df_infors_reactor_measurements['Stirrer'].astype(float)
            df_infors_reactor_measurements['Temp'] = df_infors_reactor_measurements['Temp'].astype(float)
            df_infors_reactor_measurements['pH'] = df_infors_reactor_measurements['pH'].astype(float)
            df_infors_reactor_measurements['pO2'] = df_infors_reactor_measurements['pO2'].astype(float)
            df_infors_reactor_measurements.loc[:, 'DateTime'] = pd.to_datetime(df_infors_reactor_measurements.DateTime,
                                                                               format="%Y-%m-%d %H:%M:%S")
            df_infors_reactor_measurements = df_infors_reactor_measurements[(df_infors_reactor_measurements.DateTime >
                                                                             df_physical_chemical_analysis['Tempo (h)'].min()) & (
                        df_infors_reactor_measurements.DateTime < df_physical_chemical_analysis['Tempo (h)'].max())]
            st.markdown("Tabela de registro das medições do reator Minifors 2")
            st.dataframe(df_infors_reactor_measurements)

            co2_measurements = st.file_uploader(
                "Por favor escolher arquivo exportado do medidor de CO2 com final '*.csv'",
                type='csv')

            if (co2_measurements is not None):
                df_co2_measurements = pd.read_csv(co2_measurements, sep=';')
                df_co2_measurements.loc[:, 'data_registro'] = pd.to_datetime(df_co2_measurements.data_registro,
                                                                      format="%Y-%m-%d %H:%M:%S")
                df_co2_measurements = df_co2_measurements.drop(['id', 'temperatura', 'UR', 'reator_CO2_2'], axis=1)
                value_temp = df_co2_measurements.reator_CO2_1.min()
                register_co2_filter = []
                for index, row in df_co2_measurements.iterrows():
                    if value_temp != row['reator_CO2_1']:
                        register_co2_filter.append([row['reator_CO2_1'], row['data_registro']])
                    value_temp = row['reator_CO2_1']
                df_co2_measurements = pd.DataFrame(register_co2_filter, columns=['reator_CO2', 'data_registro'])
                st.markdown("Tabela de registros do medidor de CO2")
                st.dataframe(df_co2_measurements.head())
                chart_df_co2_measurements = df_co2_measurements.copy()
                chart_df_co2_measurements.index = ((df_co2_measurements.data_registro - df_co2_measurements.data_registro.min()).dt.total_seconds())/3600
                st.area_chart(chart_df_co2_measurements.reator_CO2)

if __name__ == '__main__':
    main()