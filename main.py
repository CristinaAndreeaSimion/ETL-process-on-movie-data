import pandas as pd

# Citire fisier CSV
df = pd.read_csv('movies.csv')

# Conversii pentru coloane numerice
df['box_office'] = pd.to_numeric(df['box_office'], errors='coerce')
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
df['country'] = df['country'].replace({
    'USA': 'SUA',
    'UK': 'Anglia',
    'South Korea': 'Coreea de Sud',
    'Russia': 'Rusia'
})

# Tarile tinta
tari = ['SUA', 'Rusia', 'Anglia', 'Coreea de Sud']

# Procesare per tara
for tara in tari:
    df_tara = df[df['country'] == tara].copy()

    if df_tara.empty:
        print(f'Nu exista filme pentru {tara}')
        continue

    # Calculam coloana bilant
    df_tara['bilant'] = df_tara['box_office'] - df_tara['budget']

    # Selectam coloanele cerute
    df_tara = df_tara[['title', 'release_year', 'genre', 'director', 'bilant']]

    # Salvare in acelasssi folder cu scriptul
    nume_fisier = f'top_10_filme_{tara}.xlsx'

    # Scriere in Excel
    with pd.ExcelWriter(nume_fisier, engine='openpyxl') as writer:
        top_general = df_tara.sort_values(by='bilant', ascending=False).head(10)
        top_general.to_excel(writer, sheet_name='general', index=False)

        for gen in df_tara['genre'].dropna().unique():
            top_gen = df_tara[df_tara['genre'] == gen].sort_values(by='bilant', ascending=False).head(10)
            sheet_name = gen[:31]
            top_gen.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f'Fisier salvat: {nume_fisier}')
