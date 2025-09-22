import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

def plot_outliers(df_scaled, methods_masks, save_path="outliers_plot.png"):
    """
    Plot outliers with pie-style markers to show which methods detected them.
    
    Parameters:
        df_scaled (DataFrame): scaled numeric data
        methods_masks (dict): {method_name: boolean_series_of_outliers}
        save_path (str): path to save the figure
    """
    x_col, y_col = df_scaled.columns[:2]
    
    plt.figure(figsize=(10,6))
    
    combined_mask = None
    for mask in methods_masks.values():
        combined_mask = mask if combined_mask is None else combined_mask | mask
    normal_mask = ~combined_mask # type: ignore
    plt.scatter(
        df_scaled.loc[normal_mask, x_col],
        df_scaled.loc[normal_mask, y_col],
        color="lightgrey",
        alpha=0.5,
        label="Normal points"
    )
    
    method_colors = ["red", "blue", "green", "yellow"]
    
    for idx in df_scaled.index[combined_mask]:
        x, y = df_scaled.loc[idx, x_col], df_scaled.loc[idx, y_col]
        triggered_methods = [i for i, (method, mask) in enumerate(methods_masks.items()) if mask[idx]]
        n = len(triggered_methods)
        for i, m_idx in enumerate(triggered_methods):
            wedge = Wedge(center=(x, y), r=0.05, theta1=i*360/n, theta2=(i+1)*360/n,
                          facecolor=method_colors[m_idx], edgecolor="k")
            plt.gca().add_patch(wedge)
    
    import matplotlib.patches as mpatches
    legend_handles = [mpatches.Patch(color=method_colors[i], label=method) 
                      for i, method in enumerate(methods_masks.keys())]
    legend_handles.insert(0, mpatches.Patch(color="lightgrey", label="Normal points"))
    plt.legend(handles=legend_handles)
    
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title("Outlier Detection Visualization (Pie markers)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    
    print(f"Outlier visualization saved to: {save_path}")