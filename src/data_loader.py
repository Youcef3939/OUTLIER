import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    load a CSV or Excel file into a pandas DataFrame.

    Args:
        file_path (str): path to the dataset.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Please use CSV or Excel.")
    except Exception as e:
        raise RuntimeError(f"Error loading file: {e}")

    if df.empty:
        print("Warning: The dataset is empty.")

    print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def list_data_files(folder_path: str) -> list:
    """
    List all CSV and Excel files in a folder.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        list: Filenames in the folder.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    files = [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.xls', '.xlsx'))]
    print(f"Found {len(files)} data file(s) in '{folder_path}': {files}")
    return files


if __name__ == "__main__":
    folder_path = "../data" 
    files = list_data_files(folder_path)
    
    if files:
        file_path = f"{folder_path}/{files[0]}"
        df = load_data(file_path)
        print(df.head())
    else:
        print("No files found in the data folder.")