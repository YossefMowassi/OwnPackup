import pandas as pd
import os
from django.http import JsonResponse


def compare_csv(request):
    file1_path = "file1.csv"
    file2_path = "file2.csv"

    if not (os.path.exists(file1_path) or os.path.exists(file2_path)):
        return JsonResponse({"error": "File path1 or path2 does not exist."})
    if not (os.path.isfile(file1_path) or os.path.isfile(file2_path)):
        return JsonResponse({"error": "File1 or File2 path is not a valid file."})
    if not (file1_path.endswith('.csv') or file2_path.endswith('.csv')):
        return JsonResponse({"error": "File1 or File2 does not have a CSV extension."})

    file1_data = pd.read_csv(file1_path)
    file2_data = pd.read_csv(file2_path)

    if file1_data.empty or file2_data.empty:
        return JsonResponse({"error": "File1 or File2 is empty"})

    file1_id = list(file1_data['ID'])
    file2_id = list(file2_data['ID'])
    json_Output = {}
    added, changed, deleted = [], [], []
    file_1_ids_set = set(file1_id)
    file_2_ids_set = set(file2_id)

    for num in file1_id:
        if num not in file2_id:
            added.append(num)
    for num in file_1_ids_set & file_2_ids_set:
        if file1_data.loc[file1_data['ID'] == num].values.tolist() != file2_data.loc[file2_data['ID'] == num].values.tolist():
            changed.append(num)
    for num in file2_id:
        if num not in file1_id:
            deleted.append(num)

    json_Output['added'] = added
    json_Output["deleted"] = deleted
    json_Output["changed"] = changed

    return JsonResponse(json_Output)
