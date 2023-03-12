
import base64
CLASS = "Class"
LEVEL = "Level"

def filter_dataframe_per_class(dataframe, class_name):
    return dataframe[dataframe["Class"] == class_name].dropna(axis=1, how="all")

def get_total(dataframe):
    count = dataframe[CLASS].value_counts().sum()
    return count

def get_qsets_columns(dataframe):
    qset_columns = set()
    [qset_columns.add(column.split(".", 1)[0]) for column in dataframe.columns if "Qto" in column]
    return list(qset_columns) if qset_columns else None

def get_quantities(frame, quantity_set):
    columns = []
    [columns.append(column.split(".", 1)[1]) for column in frame.columns if quantity_set in column]
    columns.append("Count")
    return columns

def download_csv(file_name, dataframe):
    file_name = file_name.replace('.ifc', '.csv')
    dataframe.to_csv(f'./downloads/{file_name}')

def download_excel(file_name, dataframe):
    import pandas
    file_name = file_name.replace('.ifc', '.xlsx')
    writer = pandas.ExcelWriter(f'./downloads/{file_name}', engine="xlsxwriter") ## pip install xlsxwriter
    for object_class in dataframe[CLASS].unique():
        df_class = dataframe[dataframe[CLASS] == object_class].dropna(axis=1, how="all")
        df_class.to_excel(writer, sheet_name=object_class)
    writer.save()

def get_csv_table_download_link(file_name, dataframe):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a download="{file_name}.csv" href="data:file/csv;base64,{b64}">Last ned regneark</a>'
    return href